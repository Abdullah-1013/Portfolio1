import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import axios from 'axios';

const App = () => {
  const [busId, setBusId] = useState('');
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  const [message, setMessage] = useState('');

  const updateLocation = async () => {
    try {
      const response = await axios.post('http://your-server-ip:8000/update_location', {
        bus_id: busId,
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
      });
      setMessage(response.data.status);
    } catch (error) {
      setMessage('Failed to update location');
    }
  };

  const getLocation = async () => {
    try {
      const response = await axios.get(`http://your-server-ip:8000/get_location/${busId}`);
      setMessage(JSON.stringify(response.data));
    } catch (error) {
      setMessage('Failed to get location');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Bus Location Tracker</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter Bus ID"
        value={busId}
        onChangeText={text => setBusId(text)}
      />
      <TextInput
        style={styles.input}
        placeholder="Enter Latitude"
        value={latitude}
        onChangeText={text => setLatitude(text)}
        keyboardType="numeric"
      />
      <TextInput
        style={styles.input}
        placeholder="Enter Longitude"
        value={longitude}
        onChangeText={text => setLongitude(text)}
        keyboardType="numeric"
      />
      <Button title="Update Location" onPress={updateLocation} />
      <Button title="Get Location" onPress={getLocation} />
      <Text style={styles.message}>{message}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  input: {
    width: '100%',
    height: 40,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    marginBottom: 10,
    paddingHorizontal: 10,
  },
  message: {
    marginTop: 20,
    fontSize: 16,
    color: 'green',
  },
});

export default App;
