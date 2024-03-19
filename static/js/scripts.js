//Seleciona os itens clicado
let menuItem = document.querySelectorAll('.item-menu')

function selectLink(){
    menuItem.forEach((item)=>
    item.classList.remove('ativo')
    )
    this.classList.add('ativo')
}

menuItem.forEach((item)=>
    item.addEventListener('click',selectLink)
)

//Expandir menu
let btnExp = document.querySelector('#btn-exp')
let menuLat = document.querySelector('.menu-lateral')

btnExp.addEventListener('click',function(){
    menuLat.classList.toggle('expandir')
})

function openModal(){
    const modal = document.getElementById('janela-modal')
    modal.classList.add('abrir')

    modal.addEventListener('click',(e) => {
        if(e.target.id == 'fechar' || e.target.id == 'janela-modal'){
            modal.classList.remove('abrir')
        }
    })
}