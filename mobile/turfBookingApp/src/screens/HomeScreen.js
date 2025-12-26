import React, { useContext } from "react";
import { View, Text, Button } from "react-native";
import { AuthContext } from "../context/AuthContext";

export default function HomeScreen() {
  const { logout } = useContext(AuthContext);

  return (
    <View>
      <Text>Welcome to Turf Booking App</Text>
      <Button title="Logout" onPress={logout} />
    </View>
  );
}
