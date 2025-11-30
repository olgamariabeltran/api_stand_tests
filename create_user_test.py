import sender_stand_request
import data


def get_user_body(first_name):
    """
    Restituisce un dizionario copiato da data.user_body
    con il campo firstName aggiornato.
    """
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def positive_assert(first_name):
    """Test positivo: il nome utente è valido."""
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()

    str_user = (
        user_body["firstName"] + "," + user_body["phone"] + "," +
        user_body["address"] + ",,," + user_response.json()["authToken"]
    )

    assert users_table_response.text.count(str_user) == 1


def negative_assert_symbol(first_name):
    """Test negativo: nome con simboli o lunghezza non valida."""
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == (
        "Has introducido un nombre de usuario no válido. "
        "El nombre solo puede contener letras del alfabeto latino, "
        "la longitud debe ser de 2 a 15 caracteres."
    )


def negative_assert_no_firstname(user_body):
    """Test negativo: corpo della richiesta senza firstName."""
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se enviaron todos los parámetros requeridos"


# ============================
# Funzioni di test pytest
# ============================

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")


def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")


def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")


def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")


def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")
def test_create_user_no_first_name_get_error_response():
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body"
    user_body = data.user_body.copy()
    # El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)



# Prueba 9. Error. El parámetro contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
# El cuerpo actualizado de la solicitud se guarda en la variable user_body
    user_body = get_user_body("")
# Comprueba la respuesta
    negative_assert_no_firstname(user_body)

# Prueba 10. Error. El tipo del parámetro firstName: número
def test_create_user_number_type_first_name_get_error_response():
# El cuerpo actualizado de la solicitud se guarda en la variable user_body
    user_body = get_user_body(12)
# El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    response = sender_stand_request.post_new_user(user_body)

    # Comprobar el código de estado de la respuesta
    assert response.status_code == 400