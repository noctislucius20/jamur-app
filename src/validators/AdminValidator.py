admin_schema = {
    "type" : "object",
    "properties" : {
        "username" : {
            "type" : "string",
            "minLength" : 5,
            "maxLength" : 30,
            "message" : {
                "minLength" : "Username too short",
                "maxLength" : "Username too long"
            }
        },
        "email" : {
            "type" : "string",
            "pattern" : "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$",
            "maxLength" : 100,
            "message" : {
                "maxLength" : "Email too long",
                "pattern" : "Email invalid",
            }
        },
        "password" : {
            "type" : "string",
            "minLength" : 8,
            "message" : {
                "minLength" : "Password too short",
            }
        },
        "fullName" : {
            "type" : "string",
            "maxLength" : 100,
            "minLength" : 1,
            "message" : {
                "maxLength" : "Name too long",
                "minLength" : "Name too short",
            }
        }
    },
    "required" : ["username", "email", "password", "fullName"]
}