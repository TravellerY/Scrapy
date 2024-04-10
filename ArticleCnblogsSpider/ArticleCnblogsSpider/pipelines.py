# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline


class ArticlecnblogsspiderPipeline:
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            image_file = ''
            for key, value in results:
                image_file = value["path"]
            item["front_image_path"] = image_file
        return item


class MysqPipline(object):
    """
    同步写入数据库的方式（不使用）
    """

    def __init__(self):
        self.db = pymysql.connect(
            host='2.tcp.vip.cpolar.cn',
            port='11900',
            user='root',
            password='zy971006zy',
            database='article_spider',
            use_unicode=True
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        insert_sql = """
        insert into cnblog_article(title, url, url_object_id, front_image_path, front_image_url, parise_nums, comment_nums, fav_num, tags, content, creat_date)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = list()
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))
        params.append(item.get("url_object_id", ""))
        params.append(item.get("front_image_path", ""))
        front_image_list = "".join(item.get("front_image_url", []))
        params.append(front_image_list)
        params.append(item.get("praise_num", ""))
        params.append(item.get("comment_nums", ""))
        params.append(item.get("fav_nums", ""))
        params.append(item.get("tags", ""))
        params.append(item.get("content", ""))
        params.append(item.get("created_date", "1970-07-01"))
        self.cursor.execute(insert_sql, tuple(params))
        self.db.commit()
        self.cursor.close()
        self.db.close()
        return item


class MysqlTwistedPipeline(object):
    """
    异步写入数据库
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )

        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error, item, spider)  # 处理异常

    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql = """
                        insert into cnblog_article(title, url, url_object_id, front_image_path, front_image_url, parise_nums, comment_nums, fav_num, tags, content, creat_date)
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        ON DUPLICATE KEY UPDATE title=VALUES(title) ,url=VALUES(url),url_object_id=VALUES(url_object_id),
                        front_image_path=VALUES(front_image_path),front_image_url=VALUES(front_image_url),praise_nums=VALUES(praise_nums),
                        comment_nums=VALUES(comment_nums),fav_nums=VALUES(fav_nums),tags=VALUES(tags),content=VALUES(content),
                        creat_date=VALUES(creat_date)
                        """
        params = list()
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))
        params.append(item.get("url_object_id", ""))
        params.append(item.get("front_image_path", ""))
        front_image = "".join(item.get("front_image_url", []))
        params.append(front_image)
        params.append(item.get("praise_num", ""))
        params.append(item.get("comment_nums", ""))
        params.append(item.get("fav_nums", ""))
        params.append(item.get("tags", ""))
        params.append(item.get("content", ""))
        params.append(item.get("created_date", "1970-07-01"))
        a = tuple(params)
        cursor.execute(insert_sql, tuple(params))

    def handle_error(self, failure, item, spider):
        print(failure)

