// src/firebaseConfig.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyDzqJSKMosqUwm424YhlxueAKry4HZbmKA",
    authDomain: "revature-63e86.firebaseapp.com",
    projectId: "revature-63e86",
    storageBucket: "revature-63e86.firebasestorage.app",
    messagingSenderId: "646630569294",
    appId: "1:646630569294:web:c1f779d993265a9b329a1f"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export default app