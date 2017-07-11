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

rl.on('line', function(line){
  console.error(`Executing: ${line}`);
  const command = JSON.parse(line);
  const promise = new Promise((resolve, reject) => {
    sandbox.sendResponse = (res) => {
      json_res = JSON.stringify(res);
      console.log(json_res);
      resolve()
    };
    sandbox.sendResult = (r) => {
      console.error("Result: "+r);
      sandbox.sendResponse({result: r});
    };
    sandbox.sendError = (e) => {
      console.error("Send Error: "+e);
      error = {};
      Object.getOwnPropertyNames(e).forEach(function (key) {
          error[key] = e[key];
      });
      console.error("Error: ");
      sandbox.sendResponse({error:error});
    };
    vm.runInThisContext(`
      try {
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
  return promise.then(()=>{
    console.error(`Sandbox Globals: ${Object.getOwnPropertyNames(sandbox.global)}`);
  });
});
  
