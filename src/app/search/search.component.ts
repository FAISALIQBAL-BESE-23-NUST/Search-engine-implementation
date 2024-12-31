import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent {
  searchQuery: string = ''; // Store the search query
  results: any[] = []; // Store search results
  isLoading: boolean = false; // Track loading state

  constructor(private http: HttpClient) {}

  // Function triggered when the search button is clicked or the Enter key is pressed
  onSearch(): void {
    if (this.searchQuery.trim() === '') {
      this.results = []; // Clear results if the search input is empty
      return;
    }

    // Start loading
    this.isLoading = true;
    this.results = [];

    // Simulate an API call for search (you can replace this with your own API call)
    setTimeout(() => {
      this.fetchSearchResults(this.searchQuery);
    }, 1000);
  }

  // Simulate fetching search results from an API (replace with actual API call)
  fetchSearchResults(query: string): void {
    // Simulating an API response
    const mockResults = [
      { title: `Result for "${query}" 1`, description: 'Short description for result 1', link: '#' },
      { title: `Result for "${query}" 2`, description: 'Short description for result 2', link: '#' },
      { title: `Result for "${query}" 3`, description: 'Short description for result 3', link: '#' },
      { title: `Result for "${query}" 4`, description: 'Short description for result 4', link: '#' },
      { title: `Result for "${query}" 5`, description: 'Short description for result 5', link: '#' }
    ];

    // Set the results after "API call"
    this.results = mockResults;
    this.isLoading = false; // Stop loading
  }
}
