import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';

export default function App() {
  const [balance, setBalance] = useState(1000);
  const [betAmount, setBetAmount] = useState('');
  const [result, setResult] = useState('');

  const gamble = () => {
    const amount = parseFloat(betAmount);
    if (isNaN(amount) || amount <= 0 || amount > balance) {
      setResult('Invalid bet amount');
      return;
    }

    const win = Math.random() < 0.5;
    if (win) {
      setBalance(balance + amount);
      setResult(`You won $${amount}!`);
    } else {
      setBalance(balance - amount);
      setResult(`You lost $${amount}.`);
    }
    setBetAmount('');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.balance}>Balance: ${balance}</Text>
      <TextInput
        style={styles.input}
        value={betAmount}
        onChangeText={setBetAmount}
        placeholder="Enter bet amount"
        keyboardType="numeric"
      />
      <Button title="Gamble" onPress={gamble} />
      <Text style={styles.result}>{result}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  balance: {
    fontSize: 24,
    marginBottom: 20,
  },
  input: {
    width: '100%',
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    marginBottom: 20,
  },
  result: {
    marginTop: 20,
    fontSize: 18,
  },
});