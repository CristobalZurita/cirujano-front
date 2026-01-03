/**
 * Strings traducidos al español - Cirujano de Sintetizadores
 */
const MAP = {
    "about": "Nosotros",
    "all_categories": "Todas",
    "contact_thank_you": "*¡Gracias* por contactarnos!",
    "contact_thank_you_description": "Tu mensaje ha sido recibido y te responderemos a la brevedad.",
    "contact_thank_you_reply": "Nuestra respuesta será enviada a tu correo *{email}*.",
    "copyright_message": "Copyright ©{year} <a href='{url}' target='_blank'>{holder}</a> – {license}",
    "email": "Correo electrónico",
    "error_fill_all_fields": "Por favor completa todos los campos.",
    "error_invalid_email": "Por favor ingresa un correo electrónico válido.",
    "error_sending_message": "Hubo un error al enviar el mensaje.",
    "latest_release": "Novedades",
    "loading": "Cargando...",
    "message": "Mensaje",
    "name": "Nombre",
    "project_available_here": "<strong>@{title}</strong> está disponible en las siguientes plataformas:",
    "send": "Enviar mensaje",
    "sending_message": "Enviando mensaje...",
    "subject": "Asunto",
    "tags": "Etiquetas:",
    "where_to_find": "Dónde encontrarnos"
}

export function useStrings() {
    /**
     * @param {String} key
     * @param {{key:String, replacement:String}[]} [replacements=null]
     * @return {*|string}
     */
    const get = (key, replacements) => {
        let string = MAP[key] || 'strings.' + key

        if(replacements) {
            for(const replacement of replacements) {
                string = string.replace(`{${replacement.key}}`, replacement.replacement)
            }
        }

        return string
    }

    return {
        get
    }
}
