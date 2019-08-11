// var buttons = ['notify', 'error', 'wait', 'confirm', 'success', 'custom'];
// for(var i = 0; i < buttons.length; i++){
//   var button = buttons[i];
//   var btn = document.createElement('button');
//   btn.innerText = 'Show ' + button + ' modal';
//   btn.id = button;
//   document.body.appendChild(btn);
//   addHandler(btn, button);
// };
$(document).ready(function() {
  addHandler($(".tree_menu-option-edit")[0], "custom");  // For "Edit" contextmenu option's functionality
});


function addHandler(el, type){
  el.addEventListener('click', function(){
    var opts = {
      type : type,
      content : type + ' modal'
    };
    
    if(type === 'custom'){
      var input = buildComponent('input', 'modal-Custom-Input');
      input.type = 'text';

      opts.content = input;
      opts.headline = 'Folder Name';
      opts.confirmText = 'Save'
      opts.reject = function() {
        return input.value === '';
      };
      opts.confirmAction = function() {
        if($recentTarget !== null)  // $recentTarget is a jQuery object
          var folderID = $recentTarget.attr('id');
          var foldername = input.value;
          // Update DOM
          if(folderID !== "" && foldername !== "") {
              $("#"+folderID + " .tree_item span").text(foldername);
          }
          updateTreeState();
          
          // addDelta("folder", { 
          //   id : folderID,
          //   name : foldername
          // });
      };
    };
    
    var modal = modalBox(opts);
    if(type === 'wait'){
      var t = setTimeout(function(){
        modal.destroy();
        clearTimeout();
      }, 2000)
    };
    
  });
}

function modalBox(args){
  //set defaults
  var types = ['notify', 'error', 'wait', 'confirm', 'success', 'custom'];
  var headlines = ['Alert', 'Error', 'Please Wait', 'Please Confirm', 'Success', 'Prompt'];
  
  var options = {
    type : 'notify', 
    headline : '',
    content : '',
    cancelText : 'Cancel',
    confirmText : 'OK',
    cancelAction : function(){},
    confirmAction : function(){},
    reject : false,
  };
  
  //set the options
  if(args) for(arg in args) options[arg] = args[arg];
  
  //overrides
  if(types.indexOf(options.type) < 0) options.type = 'notify';
  if(options.headline === '') options.headline = headlines[types.indexOf(options.type)];
  if(options.type === 'success' || options.type === 'error') options.cancelText = '';
  if(options.type === 'wait'){
    options.cancelText = '';
    options.confirmText = '';
  };
  
  //build the modal
  var overlay = buildComponent('div', 'overlay');
  var outermodal = buildComponent('div');
  var innermodal = buildComponent('div', 'modal');
  var headline = buildComponent('header', false, options.headline);
  var content = buildComponent('div', false, options.content);
  var actions = buildComponent('footer');
  headline.className = options.type;
  innermodal.appendChild(headline);
  innermodal.appendChild(content);
  
  overlay.appendChild(outermodal);
  outermodal.appendChild(innermodal); //innermodal includes headline & content
  outermodal.appendChild(actions); //actions includes action buttons
  document.body.appendChild(overlay);
  
  overlay.destroy = function(){
    if(overlay.parentNode === document.body) document.body.removeChild(overlay);
  }


  var cancel = buildComponent('button', 'modalCancel', options.cancelText);
  var confirm = buildComponent('button', 'modalConfirm', options.confirmText);
  
  if(options.cancelText !== '') actions.appendChild(cancel);
  if(options.confirmText !== '') actions.appendChild(confirm);
  
  //add event handlers
  overlay.addEventListener('click', function(e){
    if(e.target === overlay){
      options.cancelAction();
      overlay.destroy();
    }
  });
  
  cancel.addEventListener('click', function(e){
    options.cancelAction();
    overlay.destroy();
  });
  
  confirm.addEventListener('click', function(e){
    //validate; to reject return bool true or string
    var rejected = typeof options.reject === 'function' ? options.reject() : options.reject;
    if(rejected){
      var message = typeof rejected === 'string' ? rejected : 'Please complete before continuing.';
      var retry = buildComponent('p', false, message);
      content.appendChild(retry);
    } else {
      options.confirmAction();
      overlay.destroy();
    }
  });
  
  return overlay;
};

function buildComponent(tag, id, html){
  var el = document.createElement(tag.toUpperCase());
  if(id) el.id = id;
  if(typeof html === 'string') el.innerHTML = html;
  if(typeof html === 'object') el.appendChild(html);
  return el;
};