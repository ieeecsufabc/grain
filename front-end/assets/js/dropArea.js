// selecionando todos os elementos necessários
const dropArea = document.querySelector('.drag-area'),
dragText = dropArea.querySelector('.legend1'),
button = dropArea.querySelector('.select-button'),
input = dropArea.querySelector('.input-upload')

let subtitle = document.querySelector('.subtitle')
let file // esta é uma variável global e nós usaremos dentro de várias funções

button.onclick = () => {
    input.click() // se o usuário clicar no botão então o input também será clicado
}

input.addEventListener("change", function(){
    // obter o arquivo de seleção do usuário
    // [0] significa que se o usuário selecionar múltiplos arquivos, selecionaremos apenas o primeiro
    file = this.files[0]
    showFile()
    
})

// se o usuário arrastar o arquivo sobre o DragArea
dropArea.addEventListener("dragover", (event) => {
    event.preventDefault() // evitando comportamento padrão
    dropArea.classList.add('active') // ativa o tipo de contorno sólido
    if($('.check').is(":checked")){
        dragText.textContent = "Release to upload"
    } else {
        dragText.textContent = "Solte para fazer o upload"
    }
})

// se o usuário sair da área de DragArea com o arquivo arrastado
dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove('active')
    if($('.check').is(":checked")){
        dragText.textContent = "Drag & Drop here"
    } else {
        dragText.textContent = "Arraste e solte aqui"
    }
})

// se o usuário soltar o arquivo na DropArea
dropArea.addEventListener("drop", (event) => {
    event.preventDefault() // evitando comportamento padrão
    // obter o arquivo de seleção do usuário
    // [0] significa que se o usuário selecionar múltiplos arquivos, selecionaremos apenas o primeiro
    file = event.dataTransfer.files[0]
    showFile()
})

// função de mostrar a imagem
function showFile() {
    let fileType = file.type

    let validExtensions = ["image/jpeg", "image/jpg", "image/png"]; // adicionando algumas extensões válidas de imagem no array

    if (validExtensions.includes(fileType)) { // se o arquivo selecionando pelo usuário é uma imagem
        subtitle.textContent = $('.check').is(":checked") ? "Chosen image" : "Imagem escolhida"
        dropArea.classList.add('active') // ativa o tipo de contorno sólido
        let fileReader = new FileReader(); // criando objeto de new FileReader
        fileReader.onload = () => {
            let fileURL = fileReader.result; // passando a fonte do arquivo do usuário na var fileURL
            let imgTag = `<img src="${fileURL}" alt="Imagem de micrografia">`; // criando uma tag img e passando a fonte do arquivo selecionado pelo usuário dentro do atributo src
            dropArea.innerHTML = imgTag; // adicionando a tag img criada dentro do container dropAreadropArea container
        }
        fileReader.readAsDataURL(file);
    } else {
        $('.alert').removeClass("hide");
        $('.alert').addClass("show");
        $('.alert').addClass("showAlert");
        dropArea.classList.remove("active");
        dragText.textContent = $('.check').is(":checked") ? "Drag & Drop here" : "Arraste e solte aqui"
        $('.close-btn').click(function(){
            $('.alert').addClass("hide");
            $('.alert').removeClass("show");
        });
    }
}