#!/usr/bin/env node

const WebSocket = require('ws');
const http = require('http');
const fs = require('fs');

const LOG_FILE = '/tmp/chrome-live-console.log';
const DEBUG_PORT = 9222;

// Clear the log file
fs.writeFileSync(LOG_FILE, `Chrome Console Monitor Started - ${new Date().toISOString()}\n${'='.repeat(80)}\n\n`);

function log(message) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] ${message}\n`;
  fs.appendFileSync(LOG_FILE, logLine);
  console.log(logLine.trim());
}

async function getWebSocketDebuggerUrl() {
  return new Promise((resolve, reject) => {
    http.get(`http://localhost:${DEBUG_PORT}/json`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const tabs = JSON.parse(data);
          const tab = tabs.find(t => t.type === 'page') || tabs[0];
          if (tab && tab.webSocketDebuggerUrl) {
            resolve(tab.webSocketDebuggerUrl);
          } else {
            reject(new Error('No debugger URL found'));
          }
        } catch (err) {
          reject(err);
        }
      });
    }).on('error', reject);
  });
}

async function main() {
  try {
    log('Connecting to Chrome DevTools Protocol...');

    const wsUrl = await getWebSocketDebuggerUrl();
    log(`WebSocket URL: ${wsUrl}`);

    const ws = new WebSocket(wsUrl);

    ws.on('open', () => {
      log('Connected to Chrome DevTools');

      // Enable Console domain
      ws.send(JSON.stringify({ id: 1, method: 'Console.enable' }));

      // Enable Runtime domain for console messages
      ws.send(JSON.stringify({ id: 2, method: 'Runtime.enable' }));

      // Enable Log domain
      ws.send(JSON.stringify({ id: 3, method: 'Log.enable' }));

      // Enable Network domain for network logs
      ws.send(JSON.stringify({ id: 4, method: 'Network.enable' }));

      log('Console monitoring enabled. Waiting for messages...\n');
    });

    ws.on('message', (data) => {
      try {
        const message = JSON.parse(data);

        // Console API messages (console.log, console.error, etc.)
        if (message.method === 'Runtime.consoleAPICalled') {
          const { type, args, stackTrace } = message.params;
          const logArgs = args.map(arg => {
            if (arg.value !== undefined) return arg.value;
            if (arg.description) return arg.description;
            return JSON.stringify(arg);
          }).join(' ');

          log(`[CONSOLE.${type.toUpperCase()}] ${logArgs}`);

          if (stackTrace) {
            log(`  Stack: ${stackTrace.callFrames[0]?.url}:${stackTrace.callFrames[0]?.lineNumber}`);
          }
        }

        // Runtime exceptions (uncaught errors)
        if (message.method === 'Runtime.exceptionThrown') {
          const { exceptionDetails } = message.params;
          log(`[ERROR] ${exceptionDetails.text}`);
          if (exceptionDetails.exception) {
            log(`  ${exceptionDetails.exception.description || JSON.stringify(exceptionDetails.exception)}`);
          }
          if (exceptionDetails.stackTrace) {
            exceptionDetails.stackTrace.callFrames.forEach(frame => {
              log(`    at ${frame.functionName || '(anonymous)'} (${frame.url}:${frame.lineNumber}:${frame.columnNumber})`);
            });
          }
        }

        // Log entries
        if (message.method === 'Log.entryAdded') {
          const { level, text, url, lineNumber } = message.params.entry;
          log(`[LOG.${level.toUpperCase()}] ${text}`);
          if (url) {
            log(`  Source: ${url}:${lineNumber}`);
          }
        }

        // Network request failures
        if (message.method === 'Network.loadingFailed') {
          const { requestId, errorText, canceled } = message.params;
          if (!canceled) {
            log(`[NETWORK FAILED] ${errorText} (Request ID: ${requestId})`);
          }
        }

        // Network responses with errors
        if (message.method === 'Network.responseReceived') {
          const { response } = message.params;
          if (response.status >= 400) {
            log(`[HTTP ${response.status}] ${response.url}`);
          }
        }

      } catch (err) {
        // Ignore parse errors
      }
    });

    ws.on('error', (err) => {
      log(`WebSocket error: ${err.message}`);
    });

    ws.on('close', () => {
      log('Connection closed. Monitoring stopped.');
      process.exit(0);
    });

  } catch (err) {
    log(`Error: ${err.message}`);
    process.exit(1);
  }
}

main();
