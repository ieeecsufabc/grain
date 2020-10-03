$(document).ready(function(){

    // Salvando path atual
    var loc = window.location.pathname;
    console.log(loc)

    // Construindo path até a pasta com os textos traduzidos
    if(loc == "/" || loc == "/grain" || loc == "/grain/"){
        localizationPath = loc+"localization/web";
        console.log("Worked");
        console.log(localizationPath);
    } else {
        localizationPath = "../localization/web";
    }

    // Carrega cookie (string "language=...")
    var cookie = document.cookie;
    // Salva o valor do cookie em uma variável language
    var language = cookie.substring(9)

    if (language == "en"){
        // Localização forçada
        $("[data-localize]").localize(localizationPath, { language: "en" })
    } else if (language == "pt") {
        // Localização forçada
        $("[data-localize]").localize(localizationPath, { language: "pt" })
    } else {
        // Localização automática com base na geolocalização do browser
        $("[data-localize]").localize(localizationPath)
    }

    // Mudança de localização com base no botão
    $("#en").click(function(){
        // Localização forçada
        $("[data-localize]").localize(localizationPath, { language: "en" })
        // Salva cookie
        document.cookie = "language=en";
    });
    $("#br").click(function(){
        // Localização forçada
        $("[data-localize]").localize(localizationPath, { language: "pt" })
        // Salva cookie
        document.cookie = "language=pt";
    });
});