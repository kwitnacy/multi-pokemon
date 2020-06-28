using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using UnityEngine;

public class BasePokemon : MonoBehaviour
{
    public string pName;
    public Sprite image;

    public BiomeEnum biomeFound;
    public PokemonType type;
    public Rarity rarity;

    public int HP;
    public int maxHP;

    public Stat statAttack;

    public Stat statDefence;

    public bool canBeUsedByPlayer;

    public int level;

    public bool canEvolve;

    public PokemonEvolution evolveTo;
    public PokemonStats pokemonStats;

    public List<PokemonMoves> moves = new List<PokemonMoves>();

    public List<PokemonType> damagedNormallyBy = new List<PokemonType>();
    public List<PokemonType> weakTo = new List<PokemonType>();
    public List<PokemonType> immuneTo = new List<PokemonType>();
    public List<PokemonType> resistantTo = new List<PokemonType>();

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public int GetMaxHP() { return maxHP; }

    public void AddMember(BasePokemon bp)
    {
        this.pName = bp.pName;
        this.image = bp.image;
        this.biomeFound = bp.biomeFound;
        this.type = bp.type;
        this.rarity = bp.rarity;
        this.HP = bp.HP;
        this.maxHP = bp.maxHP;
        this.statAttack = bp.statAttack;
        this.statDefence = bp.statDefence;
        this.pokemonStats = bp.pokemonStats;
        this.canEvolve = bp.canEvolve;
        this.evolveTo = bp.evolveTo;
        this.level = bp.level;
    }
}

public enum Rarity
{
    VeryCommon,
    Common,
    SemiRare,
    Rare,
    VeryRare
}

public enum PokemonType
{
    Normal,
    Flying, 
    Ground,
    Rock,
    Steel,
    Fire,
    Water,
    Grass,
    Ice,
    Electric,
    Psychic,
    Dark,
    Dragon,
    Fairy,
    Bug,
    Ghost,
    Poison,
    Fighting
}

[System.Serializable]
public class PokemonEvolution
{
    public BasePokemon nextEvolution;
    public int levelUp;
}

[System.Serializable]
public class PokemonStats
{
    public int AttackStat;
    public int DefenceStat;
    public int SpeedStat;
    public int SpAttackStat;
    public int SpDefenceStat;
    public int EvasionStat;
}
