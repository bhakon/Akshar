function highlight(){
    let keywords = document.getElementById('keyword-input').value.split('\n');
    let content = document.getElementById('text-input').value
    document.getElementById('result').innerHTML = transformContent(content, keywords)
}

function transformContent(content, keywords){
  let temp = content

  keywords.forEach(keyword => {
    temp = temp.replace(new RegExp(keyword, 'ig'), wrapKeywordWithLink(keyword, `https://www.google.com/search?q=${keyword}`))
  })

  return temp
}

function wrapKeywordWithLink(keyword, link){
  return `<a href="${link}" target="_blank"> <span style="font-weight: bold; color: red; font-size: 30px">  ${keyword}  </span> </a>`
}
