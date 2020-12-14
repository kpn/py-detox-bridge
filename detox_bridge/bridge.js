const vm = require('vm');
const readline = require('readline');

let sandbox = global;
sandbox.console = console;
sandbox.require = require;
sandbox.clearInterval = clearInterval;
sandbox.clearTimeout = clearTimeout;
sandbox.Promise = Promise;
sandbox.setInterval = setInterval;
sandbox.setTimeout = setTimeout;

const rl = readline.createInterface({
  input: process.stdin,
  terminal: false
});

//fixing circular JSON stringify, maybe switch to https://github.com/WebReflection/flatted#flatted
const replacerFunc = () => {
  const visited = new WeakSet();
  return (key, value) => {
    if (typeof value === "object" && value !== null) {
      if (visited.has(value)) {
        return `~${value}`;
      }
      visited.add(value);
    }
    return value;
  };
};

rl.on('line', function(line){
  console.error(`Executing: ${line}`);
  const command = JSON.parse(line);
  const promise = new Promise((resolve, reject) => {
    sandbox.sendResponse = (res) => {
      json_res = JSON.stringify(res, replacerFunc());
      console.log(json_res);
      resolve()
    };
    sandbox.sendResult = (r) => {
      sandbox.sendResponse({result: r});
    };
    sandbox.sendError = (e) => {
      error = {};
      Object.getOwnPropertyNames(e).forEach(function (key) {
          error[key] = e[key];
      });
      sandbox.sendResponse({error:error});
    };
    vm.runInThisContext(`
      try {
        error = undefined;
        result = (() => { ${command.eval} })();
      }
      catch(e) {
        error = e;
      }
    `);

    if( sandbox.error ) {
        sandbox.sendError(sandbox.error);
    }
    else {
        Promise.resolve(sandbox.result).then(sandbox.sendResult).catch(sandbox.sendError);
    }
  });
  return promise;
});

