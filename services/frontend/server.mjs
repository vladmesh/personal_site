import { handler as ssrHandler } from './dist/server/entry.mjs';
import http from 'node:http';

const host = process.env.HOST || '0.0.0.0';
const port = parseInt(process.env.PORT || '4321', 10);

const server = http.createServer(ssrHandler);

server.listen(port, host, () => {
  console.log(`Server listening on http://${host}:${port}`);
});
