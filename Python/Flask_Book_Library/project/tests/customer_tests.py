import pytest
from project.customers.models import Customer


@pytest.mark.parametrize("name, city, age, pesel, street, appNo", [
    ("Jan Kowalski", "Warszawa", 25, "82020512345", "Marszałkowska", "12A"),
    ("Anna Nowak", "Kraków", 30, "91030623456", "Floriańska", "45"),
    ("Piotr Wiśniewski", "Wrocław", 45, "76090734567", "Świdnicka", "8"),
    ("Maria Wójcik", "Poznań", 19, "03292845678", "Wielka", "15"),
    ("Tomasz Kowalczyk", "Gdańsk", 35, "87121956789", "Długa", "3/4"),
    ("Katarzyna Kamińska", "Łódź", 28, "94052067890", "Piotrkowska", "100"),
    ("Michał Lewandowski", "Szczecin", 42, "79081178901", "Wojska Polskiego", "22B"),
    ("Magdalena Zielińska", "Lublin", 33, "88111289012", "Krakowskie Przedmieście", "9"),
    ("Krzysztof Szymański", "Katowice", 51, "71040199123", "Mariacka", "7"),
    ("Agnieszka Woźniak", "Białystok", 29, "93072100234", "Lipowa", "16/5")
])
def test_valid_customer_data(name, city, age, pesel, street, appNo):
    customer = Customer(
        name=name,
        city=city,
        age=age,
        pesel=pesel,
        street=street,
        appNo=appNo
    )

    assert customer.name == name
    assert customer.city == city
    assert customer.age == age
    assert customer.pesel == pesel
    assert customer.street == street
    assert customer.appNo == appNo

@pytest.mark.parametrize("name, city, age, pesel, street, appNo", [
    (20, "Warszawa", 25, 82020512345, "Marszałkowska", "12A"),
    ("Anna Nowak", "Kraków", 30, 2, "Floriańska", 45),
    ("Piotr Wiśniewski", 2, 45, "76090734567", "Świdnicka", "8"),
    ("Maria Wójcik", "Poznań", "Dwa", "03292845678", "Wielka", "15"),
    (None, "Gdańsk", 35, "87121956789", "Długa", 3.5),
    ("Krzysztof Szymański", None, 51, "71040199123", "Mariacka", None),
])
def test_wrong_data_format(name, city, age, pesel, street, appNo):
    with pytest.raises(Exception):
        customer = Customer(
            name=name,
            city=city,
            age=age,
            pesel=pesel,
            street=street,
            appNo=appNo
        )


@pytest.mark.parametrize("sqli_payload", [
    "1' OR '1'='1",
    "' OR '1'='1' --",
    "1; DROP TABLE books; --",
    "'; SELECT * FROM users WHERE '1'='1",
    "1' UNION SELECT null, null, null, null, null; --",
    "' OR 'a'='a",
])
@pytest.mark.parametrize("field", ["name", "city", "age", "pesel", "street", "appNo"])
def test_sqli_data_format(sqli_payload, field):
    with pytest.raises(Exception):
        valid_customer_data = {"name": "Jan Kowalski", "city": "Warszawa", "age": 25, "pesel": "82020512345",
                               "street": "Marszałkowska", "appNo": "12A", field: sqli_payload}

        with pytest.raises(Exception):
            customer = Customer(**valid_customer_data)


@pytest.mark.parametrize("variable_length", [
    1000,
    10000
])
@pytest.mark.parametrize("field", ["name", "city", "pesel", "street", "appNo"])
def test_sqli_data_format(variable_length, field):
    with pytest.raises(Exception):
        valid_customer_data = {"name": "Jan Kowalski", "city": "Warszawa", "age": 25, "pesel": "82020512345",
                               "street": "Marszałkowska", "appNo": "12A", field: 'X' * variable_length}

        with pytest.raises(Exception):
            customer = Customer(**valid_customer_data)
