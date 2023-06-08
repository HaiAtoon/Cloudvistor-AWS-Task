import axios from 'axios'
import pQueue from 'p-queue'

// URLs to fetch data from
const urls = [
  'https://jsonplaceholder.typicode.com/posts/1',
  'https://jsonplaceholder.typicode.com/posts/2',
  'https://jsonplaceholder.typicode.com/posts/3',
  'https://jsonplaceholder.typicode.com/posts/4',
  'https://jsonplaceholder.typicode.com/posts/5',
  'https://jsonplaceholder.typicode.com/posts/6',
  'https://jsonplaceholder.typicode.com/posts/7',
  'https://jsonplaceholder.typicode.com/posts/8',
  'https://jsonplaceholder.typicode.com/posts/9',
  'https://jsonplaceholder.typicode.com/posts/10',
];

// Limit the number of concurrent requests to 3
const queue = new pQueue({ concurrency: 3 });

// Fetch data from URLs
urls.forEach(url => {
  queue.add(async () => {
    try {
      const { data } = await axios.get(url);
      console.log(`Data from ${url}: `, data);
    } catch (error) {
      console.error(`Error fetching data from ${url}: `, error.message);
    }
  });
});

// Description:
//
// In this code, I am using the `axios` library to fetch data from multiple URLs.
// I'm also using the `p-queue` library to limit the number of concurrent requests.
// As you can see, I created the queue with a concurrency of 3, which means that only 3 requests will be executed at the same time.
//
// I loop through the `urls` array I created, and add each URL to the queue using the `queue.add()` method.
// The `add()` method takes an async arrow function as an argument, which would be the async function that will be executed for each URL.
//
// Inside the async function, I use a try-catch block to handle errors.
// I make a GET request to the URL using `axios.get()` and log the data to the console if the request is successful.
// In case of an error, I log the error message to the console.
//
// By using a queue to limit the number of concurrent requests, I can prevent my application from making too many requests at once and potentially overwhelming the server.
