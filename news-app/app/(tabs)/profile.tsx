import { Ionicons } from "@expo/vector-icons";
import { Link } from "expo-router";
import React from "react";
import {
  Dimensions,
  Image,
  ScrollView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

const { width } = Dimensions.get("window");

export default function Profile() {
  return (
    <View
      style={{
        flex: 1,
        backgroundColor: "#141311",
        paddingHorizontal: 20,
        paddingVertical: 10,
      }}
    >
      <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
        <Link href={"/(tabs)"} asChild>
          <TouchableOpacity>
            <Ionicons name="arrow-back-outline" size={25} color="#fff" />
          </TouchableOpacity>
        </Link>
        <Text style={{ color: "#fff", fontSize: 18, fontWeight: 600 }}>
          Profile
        </Text>
        <View style={{ width: 24 }}></View>
      </View>
      <ScrollView
        showsVerticalScrollIndicator={false}
        style={{ marginBottom: 0 }}
        contentContainerStyle={{ paddingBottom: 20 }}
      >
        <View style={{ alignItems: "center", marginTop: 30 }}>
          <Image
            source={require("../../assets/images/userpic.jpg")}
            style={{
              width: 120,
              height: 120,
              borderRadius: 60,
              marginBottom: 10,
            }}
          />
          {/* User Full Name */}
          <Text
            style={{
              color: "#fff",
              fontSize: 19,
              fontWeight: 600,
              marginBottom: 5,
            }}
          >
            Sophia Carter
          </Text>
          {/* User Email */}
          <Text style={{ color: "grey" }}>sophiacarter@gmail.com</Text>
        </View>

        {/* Setting */}
        <View style={{ marginTop: 30 }}>
          {/* Account */}
          <View>
            <Text
              style={{
                color: "#fff",
                fontWeight: 600,
                fontSize: 18,
                marginBottom: 30,
              }}
            >
              Account
            </Text>
            <View>
              <TouchableOpacity
                style={{
                  flexDirection: "row",
                  justifyContent: "space-between",
                  marginBottom: 40,
                }}
              >
                <Text style={{ color: "whitesmoke", fontSize: 15 }}>
                  Edit Profile
                </Text>
                <Ionicons
                  name="arrow-forward-outline"
                  size={24}
                  color="whitesmoke"
                />
              </TouchableOpacity>
              <TouchableOpacity
                style={{
                  flexDirection: "row",
                  justifyContent: "space-between",
                  marginBottom: 40,
                }}
              >
                <Text style={{ color: "whitesmoke", fontSize: 15 }}>
                  Change Password
                </Text>
                <Ionicons
                  name="arrow-forward-outline"
                  size={24}
                  color="whitesmoke"
                />
              </TouchableOpacity>
              <TouchableOpacity
                style={{
                  flexDirection: "row",
                  justifyContent: "space-between",
                  marginBottom: 40,
                }}
              >
                <Text style={{ color: "whitesmoke", fontSize: 15 }}>
                  Notifications
                </Text>
                <Ionicons
                  name="arrow-forward-outline"
                  size={24}
                  color="whitesmoke"
                />
              </TouchableOpacity>
            </View>
          </View>

          {/* App Settings */}
          <View>
            <Text
              style={{
                color: "#fff",
                fontWeight: 600,
                fontSize: 18,
                marginBottom: 30,
              }}
            >
              App Settings
            </Text>
            <View>
              <TouchableOpacity
                style={{
                  flexDirection: "row",
                  justifyContent: "space-between",
                  marginBottom: 40,
                }}
              >
                <Text style={{ color: "whitesmoke", fontSize: 15 }}>Theme</Text>
                <Ionicons
                  name="arrow-forward-outline"
                  size={24}
                  color="whitesmoke"
                />
              </TouchableOpacity>
              <TouchableOpacity
                style={{
                  flexDirection: "row",
                  justifyContent: "space-between",
                  marginBottom: 40,
                }}
              >
                <Text style={{ color: "whitesmoke", fontSize: 15 }}>
                  Language
                </Text>
                <Ionicons
                  name="arrow-forward-outline"
                  size={24}
                  color="whitesmoke"
                />
              </TouchableOpacity>
              <TouchableOpacity
                style={{
                  flexDirection: "row",
                  justifyContent: "space-between",
                  marginBottom: 40,
                }}
              >
                <Text style={{ color: "whitesmoke", fontSize: 15 }}>About</Text>
                <Ionicons
                  name="arrow-forward-outline"
                  size={24}
                  color="whitesmoke"
                />
              </TouchableOpacity>
            </View>
          </View>
        </View>
        <Link href={"/(auth)/login"} asChild>
          <TouchableOpacity
            style={{
              backgroundColor: "#2c3135",
              width: width - 50,
              alignItems: "center",
              borderRadius: 20,
            }}
          >
            <Text
              style={{
                color: "#fff",
                fontWeight: 600,
                fontSize: 15,
                paddingVertical: 8,
              }}
            >
              Log Out
            </Text>
          </TouchableOpacity>
        </Link>
      </ScrollView>
    </View>
  );
}
