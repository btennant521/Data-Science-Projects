use comp3421;

drop table if exists vg_release;
drop table if exists vg_game;
drop table if exists vg_publisher;
drop table if exists vg_genre;
drop table if exists vg_platform;

create table vg_genre(
genre_id bigint auto_increment,
genre_type varchar(50),
constraint pk_genre_id primary key (genre_id));

create table vg_publisher(
publisher_id bigint auto_increment,
publisher_name varchar(50),
constraint pk_publisher_id primary key (publisher_id));

create table vg_platform(
platform_id bigint auto_increment,
platform_type varchar(50),
constraint pk_platform_id primary key (platform_id));

create table vg_release(
release_year date,
platform_id bigint,
game_id bigint,
publisher_id bigint,
NA_sales decimal(6,2),
EU_sales decimal(6,2),
JP_sales decimal(6,2),
Other_sales decimal(6,2),
constraint pk_release primary key (platform_id,game_id, publisher_id));

create table vg_game(
game_id bigint auto_increment,
game_name varchar(150),
genre_id bigint,
constraint pk_game_id primary key (game_id),
constraint fk_genre_id foreign key (genre_id) references vg_genre(genre_id));

insert into vg_genre (genre_type)
(select distinct genre from vg_csv);

insert into vg_publisher (publisher_name)
(select distinct publisher from vg_csv);

insert into vg_platform (platform_type)
(select distinct platform from vg_csv);

insert into vg_game (game_name,genre_id)
(select name, g.genre_id from vg_csv c join vg_genre g on g.genre_type=c.genre);

insert into vg_release(platform_id,game_id,publisher_id,release_year,NA_sales,EU_sales,JP_sales,Other_sales)
(select pl.platform_id, c.rank, pu.publisher_id, (case when year='N/A' then null else concat(year,'-01-01')end), NA_sales,EU_sales,JP_sales,Other_sales from vg_csv c join vg_platform pl on c.platform=pl.platform_type join vg_publisher pu on pu.publisher_name=c.publisher);