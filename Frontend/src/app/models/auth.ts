// Contrato de /api/auth/ del backend Django (JSON en camelCase)

export interface LoginI {
  username?: string;
  email?: string;
  password: string;
}

export interface LoginResponseI {
  access: string;
  refresh: string;
  tokenType: string;
  accessExpiresIn: number;
}

export interface UserI {
  id: number;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  status: 'active' | 'inactive';
}
