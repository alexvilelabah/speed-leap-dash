import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.jogopulo.vagalume',
  appName: 'Glowjump',
  webDir: 'dist',
  server: {
    androidScheme: 'https'
  }
};

export default config;
