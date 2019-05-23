import { Component, OnInit } from '@angular/core';
import { finalize } from 'rxjs/operators';

import { QuoteService } from './quote.service';
import { ApolloLink } from 'apollo-link';
import { Apollo } from 'apollo-angular';
import gql from 'graphql-tag';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  quote: string | undefined;
  isLoading = false;

  rates: any[];
  loading = true;
  error: any;


  constructor(private quoteService: QuoteService, private apollo: Apollo) {}

  ngOnInit() {
    this.isLoading = true;
    this.quoteService
      .getRandomQuote({ category: 'dev' })
      .pipe(
        finalize(() => {
          this.isLoading = false;
        })
      )
      .subscribe((quote: string) => {
        this.quote = quote;
      });

    this.apollo
      .watchQuery({
        query: gql`
          {
            rates(currency: "USD") {
              currency
              rate
            }
          }
        `
      })
      .valueChanges.subscribe(result => {
        this.rates = result.data && result.data['rates'];
        this.loading = result.loading;
        this.error = result.errors;
      });
  }
}
