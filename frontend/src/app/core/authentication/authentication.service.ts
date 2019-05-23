import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Credentials, CredentialsService } from './credentials.service';
import { HttpClient } from '@angular/common/http';
import { untilDestroyed } from '../until-destroyed';
import { map, catchError } from 'rxjs/operators';

export interface LoginContext {
  username: string;
  password: string;
  remember?: boolean;
}

/**
 * Provides a base for authentication workflow.
 * The login/logout methods should be replaced with proper implementation.
 */
@Injectable()
export class AuthenticationService {
  constructor(private credentialsService: CredentialsService, private http: HttpClient) {}

  /**
   * Authenticates the user.
   * @param context The login parameters.
   * @return The user credentials.
   */
  login(context: LoginContext): Observable<Credentials> {
    // Replace by proper authentication call

    return this.http.post('http://0.0.0.0:5000/auth', { email: context.username, password: context.password }).pipe(
      catchError(this.loginFailed()),
      map((response: { access_token: string }) => {
        const credentials: Credentials = { token: response.access_token, username: context.username };
        this.credentialsService.setCredentials(credentials, context.remember);
        return credentials;
      })
    );

    const data = {
      username: context.username,
      token: '123456'
    };
    this.credentialsService.setCredentials(data, context.remember);
    return of(data);
  }

  loginFailed(): null {
    console.log('login failed!');
    return null;
  }

  /**
   * Logs out the user and clear credentials.
   * @return True if the user was logged out successfully.
   */
  logout(): Observable<boolean> {
    // Customize credentials invalidation here
    this.credentialsService.setCredentials();
    return of(true);
  }
}
