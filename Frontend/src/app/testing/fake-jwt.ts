// JWT de prueba con "exp" en segundos; la firma no se valida en el cliente
export function fakeJwt(expSeconds: number): string {
  const encode = (value: object) => btoa(JSON.stringify(value)).replace(/=+$/, '');
  return `${encode({ alg: 'HS256', typ: 'JWT' })}.${encode({ exp: expSeconds })}.firma`;
}

export const validToken = () => fakeJwt(Math.floor(Date.now() / 1000) + 3600);
export const expiredToken = () => fakeJwt(Math.floor(Date.now() / 1000) - 60);
