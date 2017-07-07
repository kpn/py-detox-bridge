const vm = require('vm');
const readline = require('readline');

const sandbox = {result:undefined, error: undefined, console:console, global:{}, require:require};

vm.createContext(sandbox);

const rl = readline.createInterface({
  input: process.stdin,
  terminal: false
});

rl.on('line', function(line){
  console.error(`Executing: ${line}`);
  const command = JSON.parse(line);
  vm.runInContext(`try {
    result = (() => { ${command.eval} })();
  }
  catch(e) {
    error = {};
    Object.getOwnPropertyNames(e).forEach(function (key) {
        error[key] = e[key];
    });
  }
  `, sandbox);
  console.error(`Sandbox: ${JSON.stringify(sandbox)}`);
  const resultObj = {result:sandbox.result, error: sandbox.error};
  console.log(JSON.stringify(resultObj));
});
  
