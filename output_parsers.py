from typing import List, Dict, Any
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field #Pydanticv2 is under same name as pydantic_v1


class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="Interesting fact about them")


    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}
    
# Schema of output required
summary_parser = PydanticOutputParser(pydantic_object=Summary)