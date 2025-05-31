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

export default function Index() {
  return (
    <ScrollView
      showsVerticalScrollIndicator={false}
      style={{ flex: 1, backgroundColor: "#0d1719" }}
    >
      <Image
        source={require("../../assets/images/home-img.jpg")}
        style={{ width: width, height: width - 150 }}
      />
      <View style={{ paddingHorizontal: 20 }}>
        <View style={{ alignItems: "center", marginBottom: 30 }}>
          <Text
            style={{
              fontSize: 27,
              color: "#fff",
              fontWeight: 800,
              textAlign: "center",
              marginBottom: 30,
              marginTop: 20,
            }}
          >
            Your AI-Powered News Feed
          </Text>
          <Text
            style={{
              color: "#aeb8bd",
              fontSize: 16,
              textAlign: "center",
              fontWeight: 500,
            }}
          >
            Stay informed with the latest news, tailored just for you by our
            smart AI
          </Text>
        </View>

        {/* Categories */}
        <View style={{ flexDirection: "row" }}>
          <TouchableOpacity
            style={{
              backgroundColor: "#283339",
              marginRight: 10,
              paddingVertical: 8,
              paddingHorizontal: 12,
              borderRadius: 7,
            }}
          >
            <Text style={{ color: "whitesmoke", fontWeight: 500 }}>Tech</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={{
              backgroundColor: "#283339",
              marginRight: 10,
              paddingVertical: 8,
              paddingHorizontal: 12,
              borderRadius: 7,
            }}
          >
            <Text style={{ color: "whitesmoke", fontWeight: 500 }}>Sports</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={{
              backgroundColor: "#283339",
              marginRight: 10,
              paddingVertical: 8,
              paddingHorizontal: 12,
              borderRadius: 7,
            }}
          >
            <Text style={{ color: "whitesmoke", fontWeight: 500 }}>
              Politics
            </Text>
          </TouchableOpacity>
        </View>

        {/* Featured */}
        <View style={{ marginTop: 30, marginBottom: 70 }}>
          <View style={{ flexDirection: "row", marginBottom: 30 }}>
            <View style={{ width: width * 0.55, marginRight: 10 }}>
              <Text
                style={{
                  color: "grey",
                  fontSize: 15,
                  fontWeight: 600,
                  marginBottom: 10,
                }}
              >
                Trending
              </Text>
              <Text
                style={{
                  color: "#fff",
                  fontSize: 18,
                  fontWeight: 700,
                  marginBottom: 10,
                }}
              >
                Tech Giants Unveil New AI Chip
              </Text>
              <Text style={{ color: "grey", fontSize: 15, fontWeight: 500 }}>
                The new chip promises to revolutionize AI processing speed and
                efficiency.
              </Text>
            </View>
            <Image
              source={require("../../assets/images/chip.jpg")}
              style={{ width: width * 0.35, height: 130, borderRadius: 10 }}
            />
          </View>
          <View style={{ flexDirection: "row", marginBottom: 30 }}>
            <View style={{ width: width * 0.55, marginRight: 10 }}>
              <Text
                style={{
                  color: "grey",
                  fontSize: 15,
                  fontWeight: 600,
                  marginBottom: 10,
                }}
              >
                Breaking
              </Text>
              <Text
                style={{
                  color: "#fff",
                  fontSize: 18,
                  fontWeight: 700,
                  marginBottom: 10,
                }}
              >
                Local Team Wins Championship
              </Text>
              <Text style={{ color: "grey", fontSize: 15, fontWeight: 500 }}>
                The team's victory marks a historic moment for the city.
              </Text>
            </View>
            <Image
              source={require("../../assets/images/sport.jpg")}
              style={{ width: width * 0.35, height: 130, borderRadius: 10 }}
            />
          </View>
          <View style={{ flexDirection: "row", marginBottom: 30 }}>
            <View style={{ width: width * 0.55, marginRight: 10 }}>
              <Text
                style={{
                  color: "grey",
                  fontSize: 15,
                  fontWeight: 600,
                  marginBottom: 10,
                }}
              >
                Politics
              </Text>
              <Text
                style={{
                  color: "#fff",
                  fontSize: 18,
                  fontWeight: 700,
                  marginBottom: 10,
                }}
              >
                New Policy on Climate Change
              </Text>
              <Text style={{ color: "grey", fontSize: 15, fontWeight: 500 }}>
                The government announces new measures to combat climate change.
              </Text>
            </View>
            <Image
              source={require("../../assets/images/climate.jpg")}
              style={{ width: width * 0.35, height: 130, borderRadius: 10 }}
            />
          </View>
        </View>
      </View>
    </ScrollView>
  );
}
