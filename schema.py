# schema.py

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "save_it_management_system",
            "description": "将一个信息中心子管理制度保存为结构化记录",
            "parameters": {
                "type": "object",
                "properties": {
                    "system_name": {
                        "type": "string",
                        "description": "子制度名称，如：软件权限管理制度"
                    },
                    "drafting_department": {
                        "type": "string",
                        "description": "起草/制定部门，如：信息部"
                    },
                    "executing_department": {
                        "type": "string",
                        "description": "执行部门，如：各部门、各门店"
                    },
                    "supervising_department": {
                        "type": ["string", "null"],
                        "description": "监督部门，若原文未填则填 null"
                    },
                    "purpose": {
                        "type": "string",
                        "description": "原文目的说明"
                    },
                    "applicable_scope": {
                        "type": "string",
                        "description": "适用范围，如：公司全体员工"
                    },
                    "process_flow": {
                        "type": ["string", "null"],
                        "description": "流程示意描述文字，若仅有图片无文字则填 null"
                    },
                    "requirements": {
                        "type": "array",
                        "description": "具体管理要求条款",
                        "items": {
                            "type": "object",
                            "properties": {
                                "item_no": {"type": "string", "description": "条款编号，如 4.2.1"},
                                "content": {"type": "string", "description": "条款完整内容"},
                                "category": {
                                    "type": "string",
                                    "enum": ["权限安全", "问题处理", "需求开发", "数据修改", "设备管理", "其他"],
                                    "description": "该条款所属业务分类"
                                }
                            },
                            "required": ["item_no", "content", "category"],
                            "additionalProperties": False
                        }
                    },
                    "source_text": {
                        "type": "string",
                        "description": "原文片段，用于溯源"
                    }
                },
                "required": [
                    "system_name", "drafting_department", "executing_department",
                    "supervising_department", "purpose", "applicable_scope",
                    "process_flow", "requirements", "source_text"
                ],
                "additionalProperties": False
            }
        }
    }
]

PARAMETERS_SCHEMA = TOOLS[0]["function"]["parameters"]