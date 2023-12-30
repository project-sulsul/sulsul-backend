UNAUTHORIZED_RESPONSE = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {
                    "error": "UnauthorizedException",
                    "message": "Unauthorized user cannot access",
                }
            }
        },
    }
}

FORBIDDEN_RESPONSE = {
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {
                    "error": "ForbiddenException",
                    "message": "no authority to access this resource",
                }
            }
        },
    }
}

NOT_FOUND_RESPONSE = {
    404: {
        "description": "NotFound",
        "content": {
            "application/json": {
                "example": {
                    "error": "NotFoundException",
                    "message": "id not found",
                }
            }
        },
    }
}
