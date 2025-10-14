"""
LLM 모듈 간단 테스트
실제 LLM 호출 없이 구조만 테스트
"""
from llm import LLMFactory, BaseLLM


def test_factory_available_providers():
    """사용 가능한 제공자 목록 확인"""
    providers = LLMFactory.get_available_providers()
    print(f"✅ 사용 가능한 제공자: {providers}")
    assert 'ollama' in providers
    assert 'openai' in providers
    print("   - ollama: OK")
    print("   - openai: OK")


def test_create_ollama():
    """Ollama LLM 생성 테스트"""
    print("\n🧪 Ollama LLM 생성 테스트")
    llm = LLMFactory.create('ollama', 'llama2', temperature=0.5)
    
    assert isinstance(llm, BaseLLM)
    assert llm.get_model_name() == 'llama2'
    assert llm.get_config()['temperature'] == 0.5
    assert hasattr(llm, 'as_langchain_model')
    
    print(f"   - 클래스: {llm.__class__.__name__}")
    print(f"   - 모델: {llm.get_model_name()}")
    print(f"   - 설정: {llm.get_config()}")
    print("   ✅ 생성 성공!")


def test_create_openai():
    """OpenAI LLM 생성 테스트"""
    print("\n🧪 OpenAI LLM 생성 테스트")
    llm = LLMFactory.create('openai', 'gpt-4', temperature=0.7, max_tokens=100)
    
    assert isinstance(llm, BaseLLM)
    assert llm.get_model_name() == 'gpt-4'
    assert llm.get_config()['temperature'] == 0.7
    assert llm.get_config()['max_tokens'] == 100
    assert hasattr(llm, 'as_langchain_model')
    
    print(f"   - 클래스: {llm.__class__.__name__}")
    print(f"   - 모델: {llm.get_model_name()}")
    print(f"   - 설정: {llm.get_config()}")
    print("   ✅ 생성 성공!")


def test_invalid_provider():
    """잘못된 제공자로 생성 시도"""
    print("\n🧪 잘못된 제공자 테스트")
    try:
        LLMFactory.create('invalid', 'model')
        assert False, "예외가 발생해야 함"
    except ValueError as e:
        print(f"   - 예상된 예외 발생: {e}")
        print("   ✅ 예외 처리 성공!")


def test_register_custom_llm():
    """커스텀 LLM 등록 테스트"""
    print("\n🧪 커스텀 LLM 등록 테스트")
    
    class TestLLM(BaseLLM):
        def _initialize(self):
            self.test_value = "test"
        
        def __call__(self, *args, **kwargs):
            return "test response"
    
    # 등록
    LLMFactory.register('test', TestLLM)
    
    # 확인
    providers = LLMFactory.get_available_providers()
    assert 'test' in providers
    
    # 생성
    llm = LLMFactory.create('test', 'test-model')
    assert isinstance(llm, BaseLLM)
    assert llm.get_model_name() == 'test-model'
    
    print(f"   - 등록된 제공자: {providers}")
    print(f"   - 생성된 LLM: {llm.__class__.__name__}")
    print("   ✅ 등록 및 생성 성공!")


def test_liskov_substitution():
    """리스코프 치환 원칙 테스트"""
    print("\n🧪 리스코프 치환 원칙 테스트")
    
    # 모든 LLM은 BaseLLM으로 치환 가능해야 함
    llms = [
        LLMFactory.create('ollama', 'llama2'),
        LLMFactory.create('openai', 'gpt-4'),
    ]
    
    for llm in llms:
        # 모든 LLM은 동일한 인터페이스를 가져야 함
        assert hasattr(llm, 'get_model_name')
        assert hasattr(llm, 'get_config')
        assert hasattr(llm, 'as_langchain_model')
        assert callable(llm)
        print(f"   - {llm.__class__.__name__}: 인터페이스 호환 ✅")
    
    print("   ✅ 모든 LLM이 동일한 인터페이스 제공!")


def main():
    """모든 테스트 실행"""
    print("=" * 60)
    print("🚀 LLM 모듈 구조 테스트")
    print("=" * 60)
    
    try:
        test_factory_available_providers()
        test_create_ollama()
        test_create_openai()
        test_invalid_provider()
        test_register_custom_llm()
        test_liskov_substitution()
        
        print("\n" + "=" * 60)
        print("✨ 모든 테스트 통과!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

