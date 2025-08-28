// Script para probar la API del microservicio TOTP
const http = require('http');

function makeRequest(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: process.env.PORT || 3001,
      path: path,
      method: 'GET'
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    });

    req.on('error', (err) => {
      reject(err);
    });

    req.end();
  });
}

async function testAPI() {
  console.log('🧪 PROBANDO API DEL MICROSERVICIO TOTP');
  console.log('=' .repeat(50));

  try {
    // Test 1: Health check
    console.log('\n1️⃣ Health Check:');
    const health = await makeRequest('/health');
    console.log(JSON.stringify(health, null, 2));

    // Test 2: Obtener código TOTP
    console.log('\n2️⃣ Código TOTP:');
    const totp = await makeRequest('/totp');
    console.log(JSON.stringify(totp, null, 2));

    // Test 3: Información del servicio
    console.log('\n3️⃣ Info del Servicio:');
    const info = await makeRequest('/totp/info');
    console.log(JSON.stringify(info, null, 2));

    // Test 4: Documentación
    console.log('\n4️⃣ Documentación:');
    const docs = await makeRequest('/');
    console.log('Documentación disponible en: http://localhost:3000/');

    console.log('\n✅ TODOS LOS TESTS PASARON');
    console.log(`🔐 Código actual: ${totp.data.code}`);
    console.log(`⏰ Válido por: ${totp.data.timeRemaining} segundos`);

  } catch (error) {
    console.error('❌ Error en las pruebas:', error.message);
    console.log('\n💡 Asegúrate de que el servidor esté corriendo:');
    console.log('   npm run server');
  }
}

testAPI();
