from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        drop_base = '''drop view if exists base_stat;'''
        drop_place = '''drop view if exists team_place;'''
        create_base= '''
            create view base_stat as select 
            ROW_NUMBER() over() as id,
            gp.game_id,
            pn.summ_penalty,
            au.id as user_id,
            gp.level_id, 
            au.username,  
            gl.name, 
            gp.level_status, 
            gp.level_finished,  
            gp.level_penalty,
            (select count(*)  from api_gameplay ag  where ag.level_status ='DN' AND team_id = au.id ) as total_finished
            from 
            api_gameplay gp  
            join api_gamelevel gl on gl.number = gp.level_id  
            left join auth_user au on au.id  = gp.team_id
            left join (select team_id, (sum(level_penalty + cast((wrong_counter_answer*1800) as DECIMAL(17,11))+ cast((getted_promt_counter*900) as DECIMAL(17,11)))) as summ_penalty  from api_gameplay ag  group by team_id) as pn 
            on pn.team_id =au.id 
            order by total_finished desc, pn.summ_penalty; '''
        create_place = '''
            create view team_place as
            select ROW_NUMBER() over() id, game_id, tw.place, tw.username, level_id, level_status ,level_penalty, tw.total_finished, tw.summ_penalty, user_id, level_id  
            FROM base_stat bs join  
            (select ROW_NUMBER() over (order by total_finished desc, summ_penalty) as place, username, total_finished, summ_penalty
            from (select 
            username,
            id, 
            level_status,
            level_penalty,
            total_finished, 
            summ_penalty 
            from base_stat
            group by level_id, username
            order by total_finished desc, summ_penalty) as tw
            GROUp by username) 
            on tw.username = bs.username
            GROUP by place, level_id; '''
        cursor = connection.cursor()
        cursor.execute(drop_base)
        cursor.execute(drop_place)
        cursor.execute(create_base)
        cursor.execute(create_place)


