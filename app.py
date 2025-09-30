import random
import math
import copy

# Fungsi untuk hitung jarak total rute
def calculate_distance(route, distance_matrix):
    total = 0
    for i in range(len(route) - 1):
        total += distance_matrix[route[i]][route[i+1]]
    return total

# Fungsi generate neighbor: swap dua index acak di tengah (pos 1 hingga n-2)
def generate_neighbor(route):
    neighbor = copy.deepcopy(route)
    n = len(route)
    if n > 2:  # Minimal 3 titik (start, 1 tengah, end)
        idx1, idx2 = random.sample(range(1, n-1), 2)  # Swap di tengah saja
        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
    return neighbor

# Simulated Annealing
def simulated_annealing(distance_matrix, initial_temp=1000, cooling_rate=0.95, min_temp=0.1, max_iter=1000):
    n = len(distance_matrix)
    # Solusi awal: [0, 1, 2, ..., n-1] (sequential, start dan end tetap)
    current_route = list(range(n))  # [0,1,2,...,n-1]
    # Shuffle titik tengah saja untuk variasi awal
    if n > 2:
        random.shuffle(current_route[1:n-1])
    
    current_distance = calculate_distance(current_route, distance_matrix)
    best_route = copy.deepcopy(current_route)
    best_distance = current_distance
    
    temp = initial_temp  # Suhu awal
    iteration = 0
    min_distance = best_distance  # Track MIN jarak
    max_distance = best_distance  # Track MAX jarak
    min_temp_reached = temp  # Track MIN suhu
    max_temp_reached = temp  # Track MAX suhu
    
    while temp > min_temp and iteration < max_iter:
        # Generate neighbor
        neighbor_route = generate_neighbor(current_route)
        neighbor_distance = calculate_distance(neighbor_route, distance_matrix)
        
        # Update min/max jarak
        if neighbor_distance < min_distance:
            min_distance = neighbor_distance
        if neighbor_distance > max_distance:
            max_distance = neighbor_distance
        
        delta = neighbor_distance - current_distance
        
        # Acceptance
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_route = neighbor_route
            current_distance = neighbor_distance
        
        # Update best
        if current_distance < best_distance:
            best_route = copy.deepcopy(current_route)
            best_distance = current_distance
        
        # Cooling: T = T * alpha
        temp *= cooling_rate
        iteration += 1
        
        # Update min/max suhu (MIN-MAX check)
        if temp < min_temp_reached:
            min_temp_reached = temp
        if temp > max_temp_reached:
            max_temp_reached = temp  # Biasanya initial yang max
    
    # Output hasil dengan MIN-MAX
    print(f"MIN Suhu: {min_temp_reached:.2f}")
    print(f"MAX Suhu: {max_temp_reached:.2f}")
    print(f"Suhu Akhir: {temp:.2f}")
    print(f"MIN Jarak: {min_distance:.2f}")
    print(f"MAX Jarak: {max_distance:.2f}")
    print(f"Best Jarak: {best_distance:.2f}")
    print(f"Total Iterasi: {iteration}")
    
    return best_route, best_distance

# Lokasi: 0=Ojan, 1=Naufal, 2=Gideon, 3=Wildy, 4=Dhafin, 5=Shofa, 6=Tiara, 7=Kampus
location_names = ["Ojan", "Naufal", "Gideon", "Wildy", "Dhafin", "Shofa", "Tiara", "Kampus"]

distance_matrix = [
    [0,   4.5, 3.3, 3.2, 3,   4.1, 3,   1.3],  # Ojan
    [4.5, 0,   4,   6.1, 2,   5,   2.8, 5.6],  # Naufal
    [3.3, 4,   0,   0.6, 2.8, 3.7, 0.27,0.9],  # Gideon
    [3.2, 6.1, 0.6, 0,   3.7, 6.7, 0.5, 2.4],  # Wildy
    [3,   2,   2.8, 3.7, 0,   7.6, 3.3, 3.7],  # Dhafin
    [4.1, 5,   3.7, 6.7, 7.6, 0,   4.6, 4.7],  # Shofa
    [3,   2.8, 0.27,0.5, 3.3, 4.6, 0,   1.5],  # Tiara
    [1.3, 5.6, 0.9, 2.4, 3.7, 4.7, 1.5, 0]    # Kampus
]

best_route, best_dist = simulated_annealing(distance_matrix)

# Tampilkan rute dengan nama lokasi
route_names = [location_names[i] for i in best_route]
print(f"\nRute Terbaik: {best_route}")
print(f"Rute dengan Nama: {' -> '.join(route_names)}")
print(f"Jarak Total Terbaik: {best_dist:.2f} km")
print(f"\nCatatan: Rute dimulai dari {location_names[0]} dan berakhir di {location_names[7]}")

# Contoh output iterasi (untuk debug, uncomment jika perlu)
# Di dalam loop SA, tambahkan: print(f"Iter {iteration}: Route {current_route}, Dist {current_distance}, Temp {temp}")
