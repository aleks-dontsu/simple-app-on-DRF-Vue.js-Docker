<template>
  <div>
    <button :disabled="!prevPage" @click="fetchCars(prevPage)">&lt;</button>
    <button :disabled="!nextPage" @click="fetchCars(nextPage)">&gt;</button>
    <table>
      <thead>
      <tr>
        <th>ID</th>
        <th>Vendor</th>
        <th>Model</th>
        <th>Year</th>
        <th>Volume</th>
        <th>Remove</th>
      </tr>
      </thead>
      <tbody>
        <tr v-for="car in cars" v-bind:key="car.id">
          <td>{{ car.id }}</td>
          <td>{{ car.vendor }}</td>
          <td>{{ car.model }}</td>
          <td>{{ car.year }}</td>
          <td>{{ car.volume }}</td>
          <td><button @click="removeCar(car)">-</button></td>
        </tr>
      </tbody>
    </table>

    <button @click="filterCars()">Filter!</button>
    <button @click="addFilter()">+</button>

    <ul>
      <li v-for="filter in filters" :key="filter.id">
        <input v-model="filter.key">
        <input v-model="filter.value">
        <button @click="dropFilter(filter)">-</button>
      </li>
    </ul>

    <button @click="shuffleCars()">Shuffle</button>

    <input type="text" placeholder="vendor" v-model="currentCar.vendor">
    <input type="text" placeholder="model" v-model="currentCar.model">
    <input type="text" placeholder="year" v-model.number="currentCar.year">
    <input type="text" placeholder="volume" v-model.number="currentCar.volume">
    <button @click="createCar()">Create</button>
  </div>
</template>

<script>
import { shuffle } from 'lodash';

const host = process.env.VUE_APP_BACKEND_HOST || '';

export default {
  name: 'Home',

  data() {
    return {
      cars: [],
      currentCar: {},
      nextPage: null,
      prevPage: null,
      filters: [],
    };
  },
  async created() {
    await this.fetchCars();
  },

  methods: {
    async fetchCars(url = `${host}/api/cars/`) {
      const response = await fetch(url);
      const { results, next, previous } = await response.json();
      this.cars = results;
      this.nextPage = next;
      this.prevPage = previous;
    },
    async createCar() {
      const response = await fetch(`${host}/api/cars/`, {
        method: 'POST',
        headers: {
          // 'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.currentCar),
      });

      if (response.status !== 201) {
        alert(JSON.stringify(await response.json(), null, 2));
      }

      await this.fetchCars();
    },
    async removeCar(car) {
      const { id } = car;
      const response = await fetch(`${host}/api/cars/${id}/`, {
        method: 'DELETE',
        headers: {
          // 'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      });

      if (response.status !== 204) {
        alert(JSON.stringify(await response.json(), null, 2));
      }

      await this.fetchCars();
    },

    shuffleCars() {
      this.cars = shuffle(this.cars);
    },

    addFilter() {
      this.filters.push({ id: Math.random() });
    },

    dropFilter(filter) {
      this.filters = this.filters.filter((f) => f.id !== filter.id);
    },

    async filterCars() {
      const filledFilters = this.filters.filter(({ key, value }) => key && value);
      const url = new URL(`${host}/api/cars/`);
      filledFilters.forEach(({ key, value }) => url.searchParams.append(key, value));
      await this.fetchCars(url);
    },
  },
};
</script>
