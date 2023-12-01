from ordered_map import OrderedMap

if __name__ == "__main__":
    nyt_map = OrderedMap()
    nyt_map["Michael Jordan"] = "10/20/2002"
    nyt_map["Lebron James"] = "09/27/1999"
    nyt_map["Karl Malone"] = "01/06/2003"
    nyt_map["Kareem Abdul Jabar"] = "07/08/1986"
    nyt_map["Isaiah Thomas"] = "08/17/2005"
    nyt_map["Dennis Rodman"] = "04/06/2009"
    nyt_map["Magic Johnson"] = "12/31/1995"
    nyt_map["Magic Johnson"] = "06/08/2022"

    nyt_map.rb_tree.print_bfs(nyt_map.rb_tree.root)

    print(nyt_map["Magic Johnson"])
