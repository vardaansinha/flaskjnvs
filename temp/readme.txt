[nix-shell:/mnt/c/Users/navan/vscode/flaskjnvs/volumes]# sqlite3 sqlite.db
SQLite version 3.38.2 2022-03-26 13:51:10
Enter ".help" for usage hints.
sqlite> .headers ON
sqlite> select * from breakingnews;
id|_title|_network|_day|_city|_link|_lat|_lng
1|Padres FanFest mayhem: Long lines, crowded concourses, and delayed entry|CNN|2023-01-21|San Diego|https://www.cbs8.com/article/news/local/padres-fanfest-mayhem-crowded-concourses-and-delayed-entry/509-543c588b-0eba-4c95-bb84-b3538894dd77|32.7157|-117.1611
2|Temecula - Forklifts Stolen From Home Depot|Fox|2023-01-20|Temecula|https://fox5sandiego.com/news/local-news/forklift-stolen-from-oceanside-home-depot-in-broad-daylight/|33.4934|-117.1488
3|Long Beach State beats UC Irvine in OT|ABC|2023-01-19|Irvine|https://www.usatoday.com/story/sports/ncaab/2023/02/05/long-beach-state-beats-uc-irvine-in-ot-for-6th-straight-win/51256357/|33.6846|-117.8265
4|El Centro will conduct a public hearing for new parks|NBC|2023-01-20|El Centro|https://www.ivpressonline.com/|32.792|-115.5631
