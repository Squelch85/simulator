const versions = {
  index: 'v1.3.4',
  gift: 'v1.3.4',
  enhancement: 'v1.3.4',
  points: 'v1.3.4',
  hit: 'v1.3.4',
  admin: 'v1.3.4'
};
function applyVersion(key){
  const el=document.getElementById('version');
  if(el && versions[key]){
    el.textContent = '버전 '+ versions[key];
  }
}

