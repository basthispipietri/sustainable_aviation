
import random
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.figure import Figure

def generate_seat_map():
    seat_map = {
        "Business": [["A", " ", "C", " ", "D", " ", "F"] for _ in range(2)],  # Business section (2 rows)
        "Economy": [["A", "B", "C", "D", "E", "F"] for _ in range(27)]  # Economy section (27 rows)
    }
    return seat_map

def fill_all_seats_with_weights(seat_map, left_weight_range=(50, 100), right_weight_range=(50, 100)):
    # Assign weights based on user-defined ranges for left and right sides
    for section, rows in seat_map.items():
        for row in rows:
            for i in range(len(row)):
                if row[i] != " ":
                    if i < 3:  # Left side
                        row[i] = random.randint(*left_weight_range)
                    else:  # Right side
                        row[i] = random.randint(*right_weight_range)
    return seat_map

def calculate_barycenter(seat_map):
    total_weight = 0
    weighted_x_sum = 0
    weighted_y_sum = 0

    # Iterate through the seat map to calculate the weighted sums
    for y_index, row in enumerate(seat_map['Economy']):
        for x_index, weight in enumerate(row):
            if weight != " ":
                x_pos = x_index if x_index < 3 else x_index + 1
                total_weight += weight
                weighted_x_sum += x_pos * weight
                weighted_y_sum += y_index * weight

    barycenter_x = weighted_x_sum / total_weight if total_weight > 0 else 0
    barycenter_y = weighted_y_sum / total_weight if total_weight > 0 else 0

    return barycenter_x, barycenter_y

def draw_seat_map_with_barycenter(seat_map, barycenter):
    fig = Figure(figsize=(12, 14))
    ax = fig.add_subplot(111)
    
    economy_y_start = 0  # Start from the top for economy section

    for rows, y_start in [(seat_map['Economy'], economy_y_start)]:
        for row_index, row in enumerate(rows):
            for col_index, seat in enumerate(row):
                if col_index < 3:  # Left of the aisle
                    x_position = col_index
                else:  # Right of the aisle
                    x_position = col_index + 1

                ax.add_patch(plt.Rectangle((x_position, y_start - row_index), 1, 1, color="white", ec="black"))
                if seat != " ":
                    ax.text(x_position + 0.5, y_start - row_index + 0.5, f"{seat}kg", 
                            va="center", ha="center", fontsize=8)
    
    rows = len(seat_map['Economy'])
    for row_index in range(rows):
        ax.text(-1.5, economy_y_start - row_index + 0.5, f"{row_index + 1}", 
                va="center", ha="right", fontsize=10, color="black")
    
    for row_index in range(-1, economy_y_start - len(seat_map['Economy']) - 1, -1):
        ax.add_patch(plt.Rectangle((3, row_index), 1, 1, color="gray", alpha=0.1))
    
    ax.set_xlim(-2, 8)
    ax.set_ylim(economy_y_start - len(seat_map['Economy']) - 1, 2)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Airbus A320 Seat Map with Barycenter", fontsize=16, weight="bold")
    plt.axis('off')
    
    # Mark barycenter
    ax.plot(barycenter[0] + 0.5, economy_y_start - barycenter[1] + 0.5, 'ro', markersize=10, label="Barycenter")
    ax.legend(loc="upper right", fontsize=10)
    
    return fig

if __name__ == "__main__":
    st.title("Airbus A320 Passenger Weight Distribution")

    st.sidebar.header("Weight Configuration")
    left_min = st.sidebar.slider("Left side minimum weight (kg)", 50, 100, 70)
    left_max = st.sidebar.slider("Left side maximum weight (kg)", 50, 100, 90)
    right_min = st.sidebar.slider("Right side minimum weight (kg)", 50, 100, 60)
    right_max = st.sidebar.slider("Right side maximum weight (kg)", 50, 100, 80)

    seat_map = generate_seat_map()
    seat_map_with_weights = fill_all_seats_with_weights(seat_map, 
                                                        left_weight_range=(left_min, left_max), 
                                                        right_weight_range=(right_min, right_max))
    barycenter = calculate_barycenter(seat_map_with_weights)

    st.write(f"### Barycenter: ({barycenter[0]:.2f}, {barycenter[1]:.2f})")
    fig = draw_seat_map_with_barycenter(seat_map_with_weights, barycenter)
    st.pyplot(fig)
