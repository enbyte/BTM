#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <iostream>
#include <cstdlib>

using namespace std;

bool init() {
    bool success = true;
    
    if (SDL_Init(SDL_INIT_EVERYTHING) != 0) {
        cout << "Unable to initialize SDL! SDL Error: " << SDL_GetError() << endl;
        success = false;
    }

    int img_flags = IMG_INIT_PNG;

    if (!(IMG_Init(img_flags) & img_flags)) {
        cout << "Unable to initialize SDL_Image! Image Error: " << IMG_GetError() << endl;
        success = false;
    }

    return success;

}

SDL_Surface *load_image(string file) {
    SDL_Surface *loaded = NULL;

    loaded = IMG_Load(file.c_str());

    if (loaded == NULL) {
        cout << "Unable to load image " << file << "!\nError: " << IMG_GetError() << endl;

    }

    return loaded;
};


class Tile {
    public:
        SDL_Surface *image;
        string name;
        char size;
        bool has_rect;

    Tile(SDL_Surface* image, string name, char size, bool is_null) {
        if (!is_null) {
            image = image;
        } else {
            image = SDL_CreateRGBSurface(0, 0, 0, 32, 0, 0, 0, 0); // 0 w/h, 32 depth
        }
        if (name == "") {
            cout << "Name cannot be a blank string!";
        }
        name = name;
        size = size;
        if (!is_null) {
            has_rect = true;
        } else {
            has_rect = false;
        }

    }


};


class _Tile {
    public:
        Tile tiletype;
        string name;
        SDL_Surface *image;
        int x;
        int y;
        SDL_Rect rect;
        bool has_rect;
        char size;
        void draw(SDL_Surface *surface);
        SDL_Rect get_rect();
        void generate_rect();
        void update_tiletype(Tile new_tiletype);

    _Tile(Tile tiletype, int x, int y) : tiletype(tiletype) {
        name = tiletype.name;
        image = tiletype.image;
        has_rect = tiletype.has_rect;
        x = x;
        y = y;
        rect = SDL_Rect();
        rect.x = x;
        rect.y = y;
        rect.w = image->w;
        rect.h = image->h;
        size = tiletype.size;

    }

};

void _Tile::draw(SDL_Surface *surface) {
    SDL_BlitSurface(this->image, NULL, surface, NULL);
}

SDL_Rect _Tile::get_rect() {
    return this->rect;
}

void _Tile::generate_rect() {
    SDL_Rect r;
    r.x = this->x;
    r.y = this->y;
    r.w = this->image->w;
    r.h = this->image->h;
    this->rect = r;

}

void _Tile::update_tiletype(Tile new_tiletype) {
    this->tiletype = new_tiletype;
    this->image = new_tiletype.image;
    this->name = new_tiletype.name;
    this->size = new_tiletype.size;
    if ((!this->has_rect) && new_tiletype.has_rect) {
        this->generate_rect();
    } else if (this->has_rect && !new_tiletype.has_rect) {
        this->rect.w = 0;
        this->rect.h = 0;
    }
    this->has_rect = new_tiletype.has_rect;
};

class Tilemap {
    public:
        int matrix[][];
};

int main() {
    return 0;
}