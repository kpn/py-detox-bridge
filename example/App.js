/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React, { useState } from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  TouchableOpacity,
  StatusBar,
} from 'react-native';

import {
  Header,
  Colors,
} from 'react-native/Libraries/NewAppScreen';

const App: () => React$Node = () => {
  const [greeting, setGreeting] = useState(null);
  const renderAfterButton = () => {
    return (
      <View style={{flex: 1, paddingTop: 20, justifyContent: 'center', alignItems: 'center'}}>
        <Text style={{fontSize: 25}}>
          {greeting}!!!
        </Text>
      </View>
    );
  };
  const updateGreeting = (greeting) => {
    return () => { setGreeting(greeting) }
  };

  if(greeting !== null) return renderAfterButton()
  
  return (
    <>
      <StatusBar barStyle="dark-content" />
      <SafeAreaView>
        <ScrollView
          contentInsetAdjustmentBehavior="automatic"
          style={styles.scrollView}>
          <Header />
          {global.HermesInternal == null ? null : (
            <View style={styles.engine}>
              <Text style={styles.footer}>Engine: Hermes</Text>
            </View>
          )}
          <View style={styles.body}>
            <View testID='welcome' style={{flex: 1, paddingTop: 20, justifyContent: 'center', alignItems: 'center'}}>
              <Text style={{fontSize: 25, marginBottom: 30}}>
                Welcome
              </Text>
              <TouchableOpacity testID='hello_button' onPress={updateGreeting('Hello')}>
                <Text style={{color: 'blue', marginBottom: 20}}>Say Hello</Text>
              </TouchableOpacity>
              <TouchableOpacity testID='world_button' onPress={updateGreeting('World')}>
                <Text style={{color: 'blue', marginBottom: 20}}>Say World</Text>
              </TouchableOpacity>
              <TouchableOpacity testID='goodbye_button' onPress={updateGreeting('Goodbye, World')}>
                <Text style={{color: 'blue', marginTop: 50, marginBottom: 20}}>Say Goodbye</Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </SafeAreaView>
    </>
  );
};

const styles = StyleSheet.create({
  scrollView: {
    backgroundColor: Colors.lighter,
  },
  engine: {
    position: 'absolute',
    right: 0,
  },
  body: {
    backgroundColor: Colors.white,
  },
  footer: {
    color: Colors.dark,
    fontSize: 12,
    fontWeight: '600',
    padding: 4,
    paddingRight: 12,
    textAlign: 'right',
  },
});

export default App;
