delimiter //
drop function if exists my_sum//
create function my_sum(a decimal(6,2),b decimal(6,2),c decimal(6,2),d decimal(6,2))returns decimal(6,2)
deterministic
begin
	declare tot decimal(6,2);
    set tot = a+b+c+d;
    return tot;
end//

drop procedure if exists gameProfitByRegion//
create procedure gameProfitByRegion( in min_prof decimal(5,2),in region varchar(2))
begin
	if region = 'WD' then
		select game_name, my_sum(NA_sales,EU_sales,JP_sales,Other_sales) from vg_release r join vg_game ga on r.game_id=ga.game_id where my_sum(NA_sales,EU_sales,JP_sales,Other_sales) > min_prof;
	elseif region = 'NA' then
		select game_name, NA_sales from vg_release r join vg_game ga on r.game_id=ga.game_id where NA_sales > min_prof;
	elseif region = 'JP' then
		select game_name, JP_sales from vg_release r join vg_game ga on r.game_id=ga.game_id where JP_sales > min_prof;
	elseif region = 'EU' then
		select game_name, EU_sales from vg_release r join vg_game ga on r.game_id=ga.game_id where EU_sales > min_prof;
	end if;
end//

drop procedure if exists genreRankingByRegion//
create procedure genreRankingByRegion( in genre varchar(50),in region varchar(2))
begin
	if region = 'WD' then
		select game_name, rank() over (partition by my_sum(NA_sales,EU_sales,JP_sales,Other_sales) order by genre_type) genre_rank from vg_release r join vg_game ga on r.game_id=ga.game_id join vg_genre ge on ga.genre_id=ge.genre_id where genre_type=genre;
	elseif region = 'NA' then
		select game_name, rank() over (partition by NA_sales order by genre_type) genre_rank from vg_release r join vg_game ga on r.game_id=ga.game_id join vg_genre ge on ga.genre_id=ge.genre_id where genre_type=genre;
	elseif region = 'JP' then
		select game_name, rank() over (partition by JP_sales order by genre_type) genre_rank from vg_release r join vg_game ga on r.game_id=ga.game_id join vg_genre ge on ga.genre_id=ge.genre_id where genre_type=genre;
	elseif region = 'EU' then
		select game_name, rank() over (partition by EU_sales order by genre_type) genre_rank from vg_release r join vg_game ga on r.game_id=ga.game_id join vg_genre ge on ga.genre_id=ge.genre_id where genre_type=genre;
	end if; 
end//

drop procedure if exists publishedReleases//
create procedure publishedReleases(in publisher varchar(100),in genre varchar(50))
begin
	select count(game_name) as 'Games Published' from vg_release r join vg_publisher pu on r.publisher_id=pu.publisher_id join vg_game ga on ga.game_id=r.game_id join vg_genre ge on ga.genre_id=ge.genre_id where (pu.publisher_name=publisher and ge.genre_type=genre);
end//

drop procedure if exists addNewRelease//
create procedure addNewRelease(in title varchar(100), in platform varchar(50), in genre varchar(50), in publisher varchar(100))
begin
-- temporary id holders to check if they exist yet
	declare pub_temp bigint;
    declare plat_temp bigint;
    declare gen_temp bigint;
    
-- id holders that will end up being inserted
	declare pub_id bigint;
    declare plat_id bigint;
    declare gen_id bigint;
    declare game_id bigint;
    
    set pub_temp = (select publisher_id from vg_publisher where publisher_name = publisher);
    set plat_temp = (select platform_id from vg_platform where platform_type = platform);
    set gen_temp = (select genre_id from vg_genre where genre_type = genre);
    if pub_temp is null then
		insert into vg_publisher (publisher_name)
        values(publisher);
	end if;
	if plat_temp is null then
		insert into vg_platform (platform_type)
        values(platform);
	end if;
	if gen_temp is null then
		insert into vg_genre (genre_type)
        values(genre);
	end if;
    
    set pub_id = (select publisher_id from vg_publisher where publisher_name=publisher);
    set plat_id = (select platform_id from vg_platform where platform_type=platform);
    set gen_id = (select genre_id from vg_genre where genre_type=genre);
    
    insert into vg_game (game_name,genre_id)
    values( title, genre_id );
    
    set game_id = (Select last_insert_id());
    
    insert into vg_release(game_id,platform_id,release_year,publisher_id)
    values(game_id, (select platform_id from vg_platform where platform_type=platform),curdate(),(select publisher_id from vg_publisher where publisher_name=publisher));
end//

