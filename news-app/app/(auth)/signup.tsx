import { Ionicons } from "@expo/vector-icons";
import { Link, useRouter } from "expo-router";
import React, { useState } from "react";
import {
  Dimensions,
  Keyboard,
  Text,
  TextInput,
  TouchableOpacity,
  TouchableWithoutFeedback,
  View,
} from "react-native";

const { width } = Dimensions.get("window");

export default function Signup() {
  const router = useRouter();
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);

  const toggleCategory = (category: string) => {
    setSelectedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((cat) => cat !== category)
        : [...prev, category]
    );
  };

  const isCategorySelected = (category: string) =>
    selectedCategories.includes(category);

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
      <View
        style={{
          flex: 1,
          backgroundColor: "#141311",
          paddingHorizontal: 15,
          paddingVertical: 10,
        }}
      >
        {/* Header */}
        <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
          <TouchableOpacity onPress={() => router.back()}>
            <Ionicons name="arrow-back-outline" size={24} color={"white"} />
          </TouchableOpacity>

          <Text
            style={{
              fontSize: 18,
              textAlign: "center",
              color: "#fff",
              fontWeight: 800,
            }}
          >
            Sign Up
          </Text>
          <View style={{ width: 24 }}></View>
        </View>

        <View style={{ flex: 1 }}>
          <View style={{ marginTop: 30 }}>
            <Text style={{ color: "#fff", fontSize: 18, fontWeight: 700 }}>
              Create your account
            </Text>
            <View style={{ marginTop: 30 }}>
              <TextInput
                placeholder="Full Name"
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
                placeholder="Email"
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
                  marginBottom: 30,
                }}
              />

              {/* Preference */}
              <Text style={{ color: "#fff", fontSize: 18, fontWeight: 700 }}>
                News Preference
              </Text>

              <View
                style={{
                  flexDirection: "row",
                  marginTop: 15,
                  maxWidth: width - 50,
                  flexWrap: "wrap",
                  rowGap: 10,
                }}
              >
                {[
                  "Tech",
                  "Sports",
                  "Politics",
                  "Business",
                  "Entertainment",
                  "Science",
                ].map((category) => (
                  <TouchableOpacity
                    key={category}
                    onPress={() => toggleCategory(category)}
                    style={{
                      backgroundColor: isCategorySelected(category)
                        ? "whitesmoke"
                        : "#283339",
                      marginRight: 10,
                      paddingVertical: 8,
                      paddingHorizontal: 12,
                      borderRadius: 7,
                    }}
                  >
                    <Text
                      style={{
                        color: isCategorySelected(category)
                          ? "#283339"
                          : "whitesmoke",
                        fontWeight: 500,
                      }}
                    >
                      {category}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          </View>
        </View>

        {/* Signup Buttons */}
        <View style={{ rowGap: 10, marginBottom: 20 }}>
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
              Sign Up
            </Text>
          </TouchableOpacity>
          <Text style={{ color: "grey", textAlign: "center" }}>
            Already have an account?
          </Text>
          <Link href={"/(auth)/login"} asChild>
            <TouchableOpacity>
              <Text
                style={{
                  color: "grey",
                  textDecorationLine: "underline",
                  textAlign: "center",
                }}
              >
                Log In
              </Text>
            </TouchableOpacity>
          </Link>
        </View>
      </View>
    </TouchableWithoutFeedback>
  );
}
