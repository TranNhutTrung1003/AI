import sys
import time
import math
import pygame
import os

# Kích thước cửa sổ
WIN_WIDTH, WIN_HEIGHT = 1000, 800

# ham nhan ma tran tu file
def Read_maze():
    file_path = "Mazes.txt"

    numberofmazes = 0
    rowofmazes = []
    Mazes = []

    with open(file_path, 'r') as file:
        number_of_mazes = int(file.readline().strip())
        numberofmazes = number_of_mazes

        for _ in range(number_of_mazes):
            row = int(file.readline().strip())
            rowofmazes.append(row)
            temp_maze = []

            for _ in range(row):
                line = file.readline().strip().split()
                maze_row = list(map(int, line))
                temp_maze.append(maze_row)

            Mazes.append(temp_maze)

    return (rowofmazes, Mazes, numberofmazes)

# ham nha cac dia diem trong file
def Read_locations():
    file_path = "Locations.txt"

    numberoflocation = 0
    rowoflocation = []
    namelocation = []
    positionlocation = []

    with open(file_path, 'r') as file:
        numberoflocation = int(file.readline().strip())

        for _ in range(numberoflocation):
            row = int(file.readline().strip())
            rowoflocation.append(row)
            temp = []

            for _ in range(row):
                line = file.readline().strip().split()
                location_row = tuple(map(int, line))
                temp.append(location_row)

            positionlocation.append(temp)
            temp_name = []

            for _ in range(row):
                line = file.readline().strip()
                temp_name.append(line)
            
            namelocation.append(temp_name)

    return (numberoflocation, rowoflocation, namelocation, positionlocation)

# ham tao ma tran bieu dien me cung
def create_maze(rows):
    matrix = []
    for i in range(rows):
        row = list(map(int, input().split(" ")))
        if(check_matrix == False):
            return None
        matrix.append(row)
    return matrix

def check_matrix(row):
    for value in row:
        if value != 0 or value != 1:
            return False
    return True

# ham sinh duong di giua diem nay den diem kia dua tren ma tran
def Search_router(matrix, start, end):
    rows = len(matrix)
    cols = len(matrix[0])

    distance = [[sys.maxsize] * cols for _ in range(rows)]
    distance[start[0]][start[1]] = 0

    #tao ra mot ma tran de xac dinh cac diem da di qua va chua di qua
    visited = [[False] * cols for _ in range(rows)]
    parent = [[None] * cols for _ in range(rows)]  # Mảng lưu trữ parent để lấy đường đi

    while True:
        u = min_distance(distance, visited)
        if u == (-1, -1) or u == end:
            break

        visited[u[0]][u[1]] = True

        #kiểm tra cac diem ke ben diem u duoc chon
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 or j == 0:
                    new_row, new_col = u[0] + i, u[1] + j
                    if (
                        # kiem tra xem hàng mới có nam trong ma tran hay khong
                        0 <= new_row < rows
                        # kiem tra cot moi co nam trong ma tran hay khong
                        and 0 <= new_col < cols
                        # kiem tra xem vi tri do co di qua hay chua
                        and not visited[new_row][new_col]
                        # kiem tra xem vi tri do co phai la tuong hay khong
                        and matrix[new_row][new_col] != 0
                        and distance[new_row][new_col] > distance[u[0]][u[1]] + matrix[new_row][new_col]
                    ):
                        distance[new_row][new_col] = distance[u[0]][u[1]] + matrix[new_row][new_col]
                        parent[new_row][new_col] = u

    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = parent[curr[0]][curr[1]]

    path.reverse()
    return path

def min_distance(dist, visited):
    min_dist = sys.maxsize
    min_index = (-1, -1)
    rows = len(dist)
    cols = len(dist[0])

    for i in range(rows):
        for j in range(cols):
            if dist[i][j] < min_dist and not visited[i][j]:
                min_dist = dist[i][j]
                min_index = (i, j)

    return min_index


# ham sinh ma tran do thi cua cac dia diem
def Graph_generation(position_locations, maze):
    rows = len(position_locations)

    Graph = [[None] * rows for _ in range(rows)]

    for i in range(rows):
        for j in range(rows):
            # khi khoang cach tu no den chinh no 
            if(i == j):
                Graph[i][j] = 0
            else:
                # khi khong co duong di truc tiep tu dia diem nay den dia diem khac
                if check_route(position_locations[i], position_locations[j], maze, position_locations) != True:
                    Graph[i][j] = sys.maxsize
                # khi co duong di truc tiep tu dia diem nay den dia diem khac
                else:
                    Graph[i][j] = math.sqrt(math.pow(position_locations[j][0] - position_locations[i][0], 2) + math.pow(position_locations[j][1] - position_locations[i][1], 2))

    return Graph


# ham kiem tra xem co duong di truc tiep tu dia diem nay den dia diem khac 
def check_route(position_location_start, position_location_end, maze, position_locations):
    shortest_path = Search_router(maze, position_location_start, position_location_end)
    if len(shortest_path) == 0 or shortest_path[0] != position_location_start or shortest_path[-1] != position_location_end:
        return False
    else:
        for cell in shortest_path:
            if cell in position_locations and cell != position_location_end and cell != position_location_start:
                return False
    return True


# ham sinh ra duong di giua dia diem nay den dia diem khac giua tren do thi
def dijkstra(graph, start, end, position_locations):
    cols = len(position_locations)
    distance = [sys.maxsize] * cols
    distance[start[1]] = 0

    visited = [False] * cols
    parent = [None] * cols

    while True:
        u = min_distance_two(distance, visited, cols)
        if u == (-1, -1) or u == end:
            break

        visited[u[1]] = True

        for i in range(cols):
            if (
                0 < graph[u[1]][i] < sys.maxsize 
                and distance[i] > distance[u[1]] + graph[u[1]][i]
                and not visited[i]
            ):
                distance[i] = distance[u[1]] + graph[u[1]][i]
                parent[i] = u

    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = parent[curr[1]]
        
    path.reverse()
    return path

def min_distance_two(dist, visited, cols):
    min_dist = sys.maxsize
    min_index = (-1, -1)

    for i in range(cols):
        if dist[i] < min_dist and not visited[i]:
            min_dist = dist[i]
            min_index = (0, i)

    return min_index

# ham dung de chuyen tu ten dia diem (bat dau, ket thuc) thanh vi tri tren do thi
def push(name, name_locations):
    cols = len(name_locations)
    position = None

    for i in range(cols):
        if name == name_locations[i]:
            position = i
            break

    return (0, position)

# Hàm để tạo cửa sổ và hiển thị ma trận
def display_maze(matrix, rows, position_locations, name_locations):

    #khoi tao game
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Mô phỏng đường đi của robot trong mê cung")

    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)

    graph = Graph_generation(position_locations, matrix)

    wall_img = pygame.image.load('Wall.png').convert_alpha()
    robot_img = pygame.image.load('Robot.png').convert_alpha()
    street_img = pygame.image.load('Street.png').convert_alpha()
    building_img = pygame.image.load('Buidling.png').convert_alpha()
    Gate_img = pygame.image.load('Gate.png').convert_alpha()
    Park_img = pygame.image.load('Park.png').convert_alpha()
    Location_img = pygame.image.load('Location.png').convert_alpha()

    sound_running = pygame.mixer.Sound('Running.wav')
    sound_victory = pygame.mixer.Sound('Victory.wav')

    wall_img = pygame.transform.scale(wall_img, (int(WIN_WIDTH // rows), int(WIN_HEIGHT // len(matrix[0]))))
    robot_img = pygame.transform.scale(robot_img, (int(WIN_WIDTH // rows), int(WIN_HEIGHT // len(matrix[0]))))
    street_img = pygame.transform.scale(street_img, (int(WIN_WIDTH // rows), int(WIN_HEIGHT // len(matrix[0]))))
    building_img = pygame.transform.scale(building_img, (int(WIN_WIDTH // rows), int(WIN_HEIGHT // len(matrix[0]))))
    Gate_img = pygame.transform.scale(Gate_img, (int(WIN_WIDTH // rows), int(WIN_HEIGHT // len(matrix[0]))))
    Park_img = pygame.transform.scale(Park_img, (int(WIN_WIDTH // rows), int(WIN_HEIGHT // len(matrix[0]))))
    Location_img = pygame.transform.scale(Location_img, (int(WIN_WIDTH // rows), int(WIN_HEIGHT // len(matrix[0]))))

    list_position_img = [building_img, Gate_img, Park_img]
    font = pygame.font.Font('Roboto-Light.ttf', 20)

    def push_position(position_path, position_locations, name_locations, list_position_img):
        rows = len(position_locations)
        position = None
        position_img = None

        for k in range(rows):
            if position_path[0] == position_locations[k][0] and position_path[1] == position_locations[k][1]:
                position = k
                if name_locations[position] == 'thu vien' or name_locations[position] == "giang duong":
                    position_img = list_position_img[0]
                elif name_locations[position] == 'cong chinh' or name_locations[position] == 'cong phu':
                    position_img = list_position_img[1]
                elif name_locations[position] == 'cong vien':
                    position_img = list_position_img[2]
                else:
                    position_img = Location_img
                break
        return [position, position_img]

    # Hàm để vẽ mê cung
    def draw_maze(matrix, rows, position_locations, name_locations):
        cell_height = WIN_HEIGHT // rows
        cell_width = WIN_WIDTH // len(matrix[0])
        img = []

        for i in range(rows):
            for j in range(len(matrix[0])):
                image = wall_img if matrix[i][j] == 0 else street_img
                if (i, j) in position_locations:
                    position_path = (i, j)
                    img = push_position(position_path, position_locations, name_locations, list_position_img)
                    win.blit(img[1], (j * cell_width, i * cell_height))

                    while (True):
                        text = font.render(str(name_locations[img[0]]), True, (0,0,0))
                        if text != None:
                            break
                    win.blit(text, (j * cell_width + cell_width // 2, i * cell_height))
                else:    
                    win.blit(image, (j * cell_width, i * cell_height))

        pygame.display.update()


    # Hàm để di chuyển robot
    def move_robot(matrix, path, position_locations, name_locations):
        cell_width = WIN_WIDTH // len(matrix[0])
        cell_height = WIN_HEIGHT // len(matrix)
        img = []

        for i in range(len(path)):
            # Vẽ robot ở vị trí mới
            x, y = path[i][1] * cell_width, path[i][0] * cell_height
            win.blit(robot_img, (x, y))

            sound_running.play()
            pygame.time.wait(1000)
            sound_running.stop()
            
            # Xóa vị trí trước đó của robot
            if i > 0:
                if path[i - 1] in position_locations:
                    img = push_position(path[i - 1], position_locations, name_locations, list_position_img)
                    win.blit(img[1], (path[i-1][1] * cell_width, path[i-1][0] * cell_height))

                    text = font.render(str(name_locations[img[0]]), True, (0,0,0))
                    win.blit(text, (path[i-1][1] * cell_width + cell_width // 2, path[i-1][0] * cell_height))
                else:
                    win.blit(street_img, (path[i-1][1] * cell_width, path[i-1][0] * cell_height))

            pygame.display.update()
            time.sleep(1)   

    # Thực hiện vẽ mê cung và di chuyển robot
    def display_maze(matrix, rows, path):
        draw_maze(matrix, rows, position_locations, name_locations)
        move_robot(matrix, path, position_locations, name_locations)

    draw_maze(matrix, rows, position_locations, name_locations)

    name_start = input("nhap vao dia diem bat dau cua robot trong me cung: ")
    name_end = input("nhap vao dia diem dich cua robot trong me cung: ")
    position_start = push(name_start, name_locations)
    position_end = push(name_end, name_locations)
    shortest_path = dijkstra(graph, position_start, position_end, position_locations)
    if len(shortest_path) == 0 or shortest_path[0] != position_start or shortest_path[-1] != position_end:
        print("Không tìm thấy đường đi từ điểm bắt đầu đến điểm đích hoặc ma trận không hợp lệ.")
    else:
        print("Đường đi ngắn nhất từ điểm bắt đầu đến điểm đích:", end=" ")
        for cell in shortest_path:
            if(cell == position_end):
                print(name_locations[cell[1]])
                break
            print(name_locations[cell[1]], end="->")
        path = Search_router(matrix, position_locations[position_start[1]], position_locations[position_end[1]])

    # pygame.quit()

    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Mô phỏng đường đi của robot trong mê cung")

    display_maze(matrix, rows, path)
    sound_victory.play()
    pygame.time.wait(1500)
    sound_victory.stop()

    # Chạy vòng lặp Pygame để giữ cửa sổ hiển thị
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


def giaodien():
    print(" "*9 + "*"*50)
    print(" "*9 + "*" + " "*48 + "*")
    print(" "*9 + "*" + " "*3 + "MÔ PHỎNG ĐƯỜNG ĐI CỦA ROBOT TRONG MÊ CUNG" + " "*4 + "*")
    print(" "*9 + "*" + " "*48 + "*")
    print(" "*9 + "*"*50)
    print()

def menu():
    print(" "*25 + "******************")
    print(" "*25 + "*      MENU      *")
    print(" "*25 + "*  1. Start      *")
    print(" "*25 + "*  2. Quit       *")
    print(" "*25 + "*                *")
    print(" "*25 + "******************")

def menuofmazes():
    print(" "*24 + "********************")
    print(" "*24 + "*   CHON ME CUNG   *")
    print(" "*24 + "*                  *")
    print(" "*24 + "*  1. Me cung 1    *")
    print(" "*24 + "*  2. Me cung 2    *")
    print(" "*24 + "*  3. Me cung khac *")
    print(" "*24 + "*  4. Quay Lai     *")
    print(" "*24 + "*                  *")
    print(" "*24 + "********************")

def Finish():
    print(" "*15 + "***********************************")
    print(" "*15 + "*                                 *")
    print(" "*15 + "*      CAM ON BAN DA SU DUNG      *")
    print(" "*15 + "*                                 *")
    print(" "*15 + "***********************************")

while(True):
    giaodien()
    menu()
    chosse = int(input("nhap vao lua chon cua ban: "))
    if chosse == 2:
        break
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        giaodien()
        menuofmazes()
        chosse2 = int(input("nhap vao lua chon cua ban: "))
        if chosse2 == 4:
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        elif chosse2 == 3:
            rows = int(input("nhap vao so hang cua ma tran me cung: "))
            while (True):
                print("nhap vao ma tran cua me cung: ")
                maze = create_maze(rows)
                if(maze != None):
                    break
                print("ma tran me cung khong hop le")

            # các địa điểm trong mê cung
            locations = int(input("Nhap vao cac dia diem co trong ban do: "))
            position_locations = []
            name_locations = []
            for i in range(locations):
                position_location = tuple(map(int, input("nhap vao vi tri dia diem thu {}: ".format(i + 1)).split(" ")))
                position_locations.append(position_location)
                name_location = input("nhap vao ten dia diem thu {}: ".format(i+1))
                name_locations.append(name_location)

            display_maze(maze, rows, position_locations, name_locations)
        else:
            temp_maze = Read_maze()
            temp_location = Read_locations()

            name_locations = temp_location[2]
            position_locations = temp_location[3]
            mazes = temp_maze[1]
            rowofmazes = temp_maze[0]

            display_maze(mazes[chosse2 - 1], rowofmazes[chosse2 - 1], position_locations[chosse2 - 1], name_locations[chosse2 - 1])

        os.system('cls' if os.name == 'nt' else 'clear')

    print()

Finish()
