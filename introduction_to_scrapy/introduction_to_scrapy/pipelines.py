# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class IntroductionToScrapyPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('price'):
            adapter['price'] = float(adapter['price'].replace('£', ''))
        if adapter.get('avaibility'):
            adapter['avaibility'] = int(adapter['avaibility'].split('(')[1].split(" ")[0])
        if adapter.get('description'):
            adapter['description'] = adapter['description'].strip()
        return item
