import { Link, useRouter } from "expo-router";
import React from "react";
import {
  Keyboard,
  KeyboardAvoidingView,
  Text,
  TextInput,
  TouchableOpacity,
  TouchableWithoutFeedback,
  View,
} from "react-native";

export default function Login() {
  const router = useRouter();

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
      <View style={{ flex: 1, backgroundColor: "#141311" }}>
        <View style={{ paddingVertical: 10 }}>
          <Text
            style={{
              fontSize: 18,
              textAlign: "center",
              color: "#fff",
              fontWeight: 800,
            }}
          >
            News App
          </Text>
        </View>

        {/* Login Section */}
        <Text
          style={{
            color: "#fff",
            fontSize: 24,
            fontWeight: 700,
            textAlign: "center",
            marginTop: 30,
          }}
        >
          Welcome Back!
        </Text>
        <KeyboardAvoidingView style={{ flex: 1 }}>
          <View style={{ paddingVertical: 30, paddingHorizontal: 15 }}>
            <TextInput
              placeholder="Username"
              placeholderTextColor={"grey"}
              style={{
                backgroundColor: "#283339",
                paddingHorizontal: 15,
                paddingVertical: 15,
                borderRadius: 10,
                color: "#fff",
                fontSize: 15,
                marginBottom: 20,
              }}
            />
            <TextInput
              placeholder="Password"
              placeholderTextColor={"grey"}
              secureTextEntry
              style={{
                backgroundColor: "#283339",
                paddingHorizontal: 15,
                paddingVertical: 15,
                borderRadius: 10,
                color: "#fff",
                fontSize: 15,
                marginBottom: 20,
              }}
            />
            <TouchableOpacity>
              <Text style={{ color: "grey", textDecorationLine: "underline" }}>
                Forgot Password?
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={{
                backgroundColor: "#ccedff",
                marginTop: 20,
                borderRadius: 10,
              }}
              onPress={() => router.push("/(tabs)")}
            >
              <Text
                style={{
                  color: "#242331",
                  textAlign: "center",
                  paddingVertical: 10,
                  fontSize: 15,
                  fontWeight: 600,
                }}
              >
                Login
              </Text>
            </TouchableOpacity>
          </View>
        </KeyboardAvoidingView>

        <View
          style={{
            position: "absolute",
            bottom: 20,
            left: 0,
            right: 0,
            alignItems: "center",
          }}
        >
          <Link href={"/(auth)/signup"} asChild>
            <TouchableOpacity>
              <Text
                style={{
                  color: "grey",
                  textDecorationLine: "underline",
                }}
              >
                Don't have an account? Sign Up
              </Text>
            </TouchableOpacity>
          </Link>
        </View>
      </View>
    </TouchableWithoutFeedback>
  );
}
