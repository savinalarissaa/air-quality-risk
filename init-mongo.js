// Beralih ke database iot_db
db = db.getSiblingDB('air_quality_db');

// Buat user untuk aplikasi
db.createUser({
  user: 'iot_user',
  pwd: 'iot_password',
  roles: [
    {
      role: 'readWrite',
      db: 'air_quality_db'
    }
  ]
});

// Buat collection untuk sensor data
db.createCollection('data_waqi');
db.createCollection('data_weatherAPI');
db.createCollection('data_risk_score');
db.createCollection('data_combined');
// db.createCollection('');

// Insert sample devices
// db.devices.insertMany([
//   {
//     device_id: 'ESP32_001',
//     device_name: 'Temperature Sensor Living Room',
//     location: 'Living Room',
//     device_type: 'temperature_humidity',
//     status: 'active',
//     created_at: new Date(),
//     last_seen: new Date()
//   },
//   {
//     device_id: 'ESP32_002',
//     device_name: 'Motion Sensor Bedroom',
//     location: 'Bedroom',
//     device_type: 'motion',
//     status: 'active',
//     created_at: new Date(),
//     last_seen: new Date()
//   },
//   {
//     device_id: 'ESP32_003',
//     device_name: 'Light Sensor Garden',
//     location: 'Garden',
//     device_type: 'light',
//     status: 'active',
//     created_at: new Date(),
//     last_seen: new Date()
//   }
// ]);

print('Database initialization completed!');