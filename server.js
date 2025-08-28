const express = require('express');
const { authenticator } = require('otplib');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;
const SECRET = process.env.GOOGLE_TOTP_SECRET || 'pumx4n26255yb52amsatqytkfjxbcrql';

// Middleware
app.use(cors());
app.use(express.json());

// Configurar authenticator para Google
authenticator.options = { digits: 6, step: 30, algorithm: 'sha1' };

// Generar código TOTP
function generateTOTPCode() {
  try {
    const code = authenticator.generate(SECRET);
    const now = Math.floor(Date.now() / 1000);
    const timeRemaining = 30 - (now % 30);

    return {
      success: true,
      code,
      timeRemaining,
      generatedAt: new Date().toISOString(),
      expiresAt: new Date((now + timeRemaining) * 1000).toISOString()
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      generatedAt: new Date().toISOString()
    };
  }
}

// API Routes
app.get('/totp', (req, res) => {
  const result = generateTOTPCode();

  if (result.success) {
    res.json({
      status: 'success',
      data: {
        code: result.code,
        timeRemaining: result.timeRemaining,
        generatedAt: result.generatedAt,
        expiresAt: result.expiresAt
      }
    });
  } else {
    res.status(500).json({
      status: 'error',
      message: result.error,
      generatedAt: result.generatedAt
    });
  }
});

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString()
  });
});

app.get('/', (req, res) => {
  res.json({
    service: 'Google TOTP Generator API',
    version: '1.0.0',
    endpoints: {
      'GET /totp': 'Obtener código TOTP actual',
      'GET /health': 'Health check'
    }
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({
    status: 'error',
    message: 'Internal server error'
  });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Google TOTP API running on port ${PORT}`);

  const initialCode = generateTOTPCode();
  if (initialCode.success) {
    console.log(`🔐 Initial code: ${initialCode.code} (${initialCode.timeRemaining}s)`);
  }

  console.log(`💡 Usage: curl http://localhost:${PORT}/totp`);
});
