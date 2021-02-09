$(document).ready(function(){

    // Salvando path atual
    var loc = window.location.pathname;
    console.log(loc)

    // Encontrando path para salvar o cookie
    if (loc.substring(1,6) == "grain"){
        console.log("github")
        cookiePath = "/grain/front-end/"

        if(loc == "/grain/front-end/" || loc == "/grain/front-end/index.html"){
            localizationPath = loc+"localization/web";
        } else {
            localizationPath = "../localization/web";
        }
    } else {
        console.log("local")
        cookiePath = "/front-end/"

        if(loc == "/front-end/" || loc == "/front-end/index.html"){
            localizationPath = loc+"localization/web";
        } else {
            localizationPath = "../localization/web";
        }
    }

    // Função de seleção de cookie
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        //if (parts.length === 2) 
        return parts.pop().split(';').shift();
    }

    // Carrega cookie (string "language=...")
    var language = getCookie("language");
    // Salva o valor do cookie em uma variável language
    console.log("Language:"+language)

    if (language == "en"){
        // Localização forçada
        $("[data-localize]").localize(localizationPath, { language: "en" })
    } else if (language == "pt") {
        // Localização forçada
        $("[data-localize]").localize(localizationPath, { language: "pt" })
    } else {
        // Localização padrão é pt
        console.log("localization not found")
        // Salva cookie inicial
        document.cookie = "language=pt;path="+cookiePath;
        $("[data-localize]").localize(localizationPath, { language: "pt" })
    }

    // Mudança de localização com base no botão
    $("#en").click(function(){
        // Localização forçada
        $("[data-localize]").localize(localizationPath, { language: "en" })
        // Salva cookie
        document.cookie = "language=en;path="+cookiePath;
    });
    $("#br").click(function(){
        // Localização forçada
        $("[data-localize]").localize(localizationPath, { language: "pt" })
        // Salva cookie
        document.cookie = "language=pt;path="+cookiePath;
    });
});