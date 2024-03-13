import jwt
import json

secret = "not_a_code_secret"

some_claims = {
    "base_claim": {
          "sub": "1234567890",
          "name": "John Doe",
          "iat": 1516239022
        },
    "student_claim": {
        "student_uni": "dff9",
        "iat": 1516239022
    },
    "project_claim": {
        "student_courses": [
            "W4111", "E6156"
        ]
    }
}

print("Original = ", json.dumps(some_claims, indent=2))

encoded_1 = jwt.encode(some_claims, secret, algorithm="HS256")
print("\nThe encoded secret is = ", encoded_1)
print("\n")

decoded_1 = jwt.decode(encoded_1, key=secret, algorithms=["HS256"])
print("Decoded = ", json.dumps(decoded_1, indent=2))

new_claim = {
    "is_this_a_claim": "totally"
}

decoded_1["cool_claim"] = new_claim

print("\n Adding claim = ", json.dumps(new_claim))

encoded_2 = jwt.encode(decoded_1, secret, algorithm="HS256")
print("\nThe encoded secret is = ", encoded_2)
print("\n")

decoded_1 = jwt.decode(encoded_2, key=secret, algorithms=["HS256"])
print("Decoded a second time = ", json.dumps(decoded_1, indent=2))