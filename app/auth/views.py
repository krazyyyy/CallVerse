from flask import request, jsonify
from app.utils.firebase import get_firestore_client
from werkzeug.security import check_password_hash, generate_password_hash
import firebase_admin
from firebase_admin import auth as firebase_auth
import datetime

def signup():
    data = request.get_json()
    email = data['email']
    password = data['password']

    db = get_firestore_client()
    print(">> DB")
    try:
        # Check if email already exists
        firebase_auth.get_user_by_email(email)
        return jsonify({"message": "Email already in use"}), 400
    except firebase_admin.auth.UserNotFoundError:
        pass  # Email does not exist, proceed with sign up

    print(">> USER")
    try:
        # Create user in Firebase Authentication
        user_record = firebase_auth.create_user(
            email=email,
            password=password,
            display_name=data['name'],
            phone_number=data['phone']
        )
        
        user_id = user_record.uid  # Get the unique user ID from Firebase
        user_data = {
            'userId': user_id,
            'name': data['name'],
            'email': email,
            'phone': data['phone'],
            'company': data['company'],
            'createdAt': datetime.datetime.utcnow(),
            'updatedAt': datetime.datetime.utcnow()
        }

        # Save user data to Firestore
        db.collection('Users').document(user_id).set(user_data)
        return jsonify({"message": "User signed up", "userId": user_id}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500


def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    db = get_firestore_client()

    # Fetch user data from Firestore
    users_ref = db.collection('Users')
    query = users_ref.where('email', '==', email).stream()

    for user in query:
        user_data = user.to_dict()
        try:
            # Verify user with Firebase Authentication
            user_record = firebase_auth.get_user_by_email(email)
            if user_record:
                if check_password_hash(user_data['password'], password):
                    return jsonify({"message": "User logged in", "userId": user_data['userId']}), 200
        except firebase_admin.auth.UserNotFoundError:
            continue
    
    return jsonify({"message": "Invalid email or password"}), 401


def logout():
    # Implement logout logic, usually involves token invalidation or client-side action
    # For Firebase, you can use Firebase Auth tokens on the client side to handle logout
    # Here we assume it's a client-side responsibility
    return jsonify({"message": "User logged out"}), 200

def change_password():
    data = request.get_json()
    user_id = data['userId']
    old_password = data['old_password']
    new_password = data['new_password']

    db = get_firestore_client()

    # Fetch user data from Firestore
    user_ref = db.collection('Users').document(user_id)
    user_data = user_ref.get().to_dict()

    if user_data and check_password_hash(user_data['password'], old_password):
        # Update password in Firestore
        user_ref.update({
            'password': generate_password_hash(new_password),
            'updatedAt': datetime.datetime.utcnow()
        })

        # Update password in Firebase Authentication
        try:
            firebase_auth.update_user(user_id, password=new_password)
            return jsonify({"message": "Password changed successfully"}), 200
        except firebase_admin.auth.UserNotFoundError:
            return jsonify({"message": "User not found"}), 404
        except Exception as e:
            return jsonify({"message": str(e)}), 500

    return jsonify({"message": "Invalid old password"}), 401

def reset_password():
    data = request.get_json()
    email = data['email']

    try:
        # Send a password reset email
        firebase_auth.send_password_reset_email(email)
        return jsonify({"message": "Password reset email sent"}), 200
    except firebase_admin.auth.UserNotFoundError:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500