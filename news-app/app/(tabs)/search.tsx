import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
import React, { useState } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";

export default function Search() {
  const [searchQuery, setSearchQuery] = useState("");
  const router = useRouter();

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      style={{ flex: 1, backgroundColor: "#0d1719" }}
    >
      <View style={{ paddingHorizontal: 15, paddingTop: 20 }}>
        {/* Search Header */}
        <View
          style={{
            flexDirection: "row",
            alignItems: "center",
            marginBottom: 20,
          }}
        >
          <TouchableOpacity onPress={() => router.back()}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text
            style={{
              color: "#fff",
              fontSize: 20,
              fontWeight: "600",
              marginLeft: 15,
            }}
          >
            Search
          </Text>
        </View>

        {/* Search Bar */}
        <View
          style={{
            flexDirection: "row",
            alignItems: "center",
            backgroundColor: "#283339",
            borderRadius: 10,
            paddingHorizontal: 15,
            marginBottom: 20,
          }}
        >
          <Ionicons name="search" size={20} color="grey" />
          <TextInput
            placeholder="Search news, topics, or sources"
            placeholderTextColor="grey"
            value={searchQuery}
            onChangeText={setSearchQuery}
            style={{
              flex: 1,
              paddingVertical: 15,
              paddingHorizontal: 10,
              color: "#fff",
              fontSize: 15,
            }}
          />
          {searchQuery.length > 0 && (
            <TouchableOpacity onPress={() => setSearchQuery("")}>
              <Ionicons name="close-circle" size={20} color="grey" />
            </TouchableOpacity>
          )}
        </View>

        {/* Search Results */}
        <ScrollView showsVerticalScrollIndicator={false}>
          {searchQuery.length > 0 ? (
            // Search results would go here
            <View style={{ paddingVertical: 20 }}>
              <Text style={{ color: "#fff", fontSize: 16 }}>
                Search results for: {searchQuery}
              </Text>
            </View>
          ) : (
            // Recent searches or suggestions
            <View style={{ paddingVertical: 20 }}>
              <Text
                style={{
                  color: "#fff",
                  fontSize: 18,
                  fontWeight: "600",
                  marginBottom: 15,
                }}
              >
                Recent Searches
              </Text>
              <View style={{ gap: 15 }}>
                {["Technology", "Sports", "Politics", "Entertainment"].map(
                  (item) => (
                    <TouchableOpacity
                      key={item}
                      onPress={() => setSearchQuery(item)}
                      style={{
                        flexDirection: "row",
                        alignItems: "center",
                        backgroundColor: "#283339",
                        padding: 15,
                        borderRadius: 10,
                      }}
                    >
                      <Ionicons
                        name="time-outline"
                        size={20}
                        color="grey"
                        style={{ marginRight: 10 }}
                      />
                      <Text style={{ color: "#fff", fontSize: 15 }}>
                        {item}
                      </Text>
                    </TouchableOpacity>
                  )
                )}
              </View>
            </View>
          )}
        </ScrollView>
      </View>
    </KeyboardAvoidingView>
  );
}
