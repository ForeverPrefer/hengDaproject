import jieba
from whoosh.analysis import Tokenizer, Token
from haystack.backends.whoosh_backend import WhooshEngine, WhooshSearchBackend

# 正确的中文分词器
class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0, mode='', **kwargs):
        words = jieba.cut_for_search(value)
        for pos, word in enumerate(words):
            token = Token()
            token.text = word.strip()
            if len(token.text) > 0:
                # 设置位置信息
                if positions:
                    token.pos = start_pos + pos
                if chars:
                    token.startchar = start_char
                    token.endchar = start_char + len(word)
                yield token

def ChineseAnalyzer():
    return ChineseTokenizer()

# 自定义 Whoosh 后端
class MyWhooshSearchBackend(WhooshSearchBackend):
    def build_schema(self, fields):
        content_field_name, schema = super().build_schema(fields)
        
        # 为所有 TEXT 字段使用中文分词器
        from whoosh.fields import TEXT
        for field_name, field_type in schema.items():
            if isinstance(field_type, TEXT):
                schema[field_name].analyzer = ChineseAnalyzer()
                
        return (content_field_name, schema)

class MyWhooshEngine(WhooshEngine):
    backend = MyWhooshSearchBackend