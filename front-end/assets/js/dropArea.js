// selecionando todos os elementos necessários
const dropArea = document.querySelector('#drag-elements'),
dragText = dropArea.querySelector('.legend1'),
button = dropArea.querySelector('.select-button'),
input = dropArea.querySelector('.input-upload'),
back = document.querySelector('#remove-image')

let subtitle = document.querySelector('.subtitle')
let file // esta é uma variável global e nós usaremos dentro de várias funções

button.onclick = () => {
    input.click() // se o usuário clicar no botão então o input também será "clicado"
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

    let validExtensions = ["image/jpeg", "image/jpg", "image/png"];

    if (validExtensions.includes(fileType)) {
        subtitle.textContent = $('.check').is(":checked") ? "Chosen image" : "Imagem escolhida"
        $(".drag-area").addClass("active")
        $("#drag-elements").css("display", "none")
        
        let fileReader = new FileReader(); // criando objeto de new FileReader
        fileReader.onload = () => {
            let fileURL = fileReader.result // passando a fonte do arquivo do usuário na var fileURL
            let imgTag = `<img src="${fileURL}" alt="Imagem de micrografia" id="preview-image">`
            $(".drag-area").append(imgTag) // adicionando a tag img criada dentro do container dropArea
        }
        fileReader.readAsDataURL(file);

        $("#remove-image").css("display", "block");
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

$("#remove-image").click(function() {
    removeFile()
})

// função de remover imagem
function removeFile() {
    subtitle.textContent = $('.check').is(":checked") ? "Choose the image" : "Escolha a imagem"
    $(".drag-area").removeClass("active")
    $("#preview-image").remove()
    $("#drag-elements").css("display", "flex")
    $("#remove-image").css("display", "none");
}